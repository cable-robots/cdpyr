import itertools
from typing import Optional, Union

import numpy as np_
import re

from cdpyr import validator as _validator
from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def rotation_x(angle):
    return np_.asarray((
        (1.0, 0.0, 0.0),
        (0.0, np_.cos(angle), -np_.sin(angle)),
        (0.0, np_.sin(angle), np_.cos(angle))
    ))


def rotation_y(angle):
    return np_.asarray((
        (np_.cos(angle), 0.0, np_.sin(angle)),
        (0.0, 1.0, 0.0),
        (-np_.sin(angle), 0.0, np_.cos(angle))
    ))


def rotation_z(angle):
    return np_.asarray((
        (np_.cos(angle), -np_.sin(angle), 0.0),
        (np_.sin(angle), np_.cos(angle), 0.0),
        (0.0, 0.0, 1.0)
    ))


rot_mapping = {
    'x': rotation_x,
    'y': rotation_y,
    'z': rotation_z
}


def from_euler(seq, angles, degrees=False):
    angles = np_.asarray(angles, dtype=float)
    if degrees:
        angles = np_.deg2rad(angles)

    # find out if intrinsic or extrinsic rotation
    intrinsic = (re.match(r'^[XYZ]{1,3}$', seq) is not None)
    extrinsic = (re.match(r'^[xyz]{1,3}$', seq) is not None)

    # now we only deal with the order of orientations
    seq = seq.lower()

    # init result
    result = np_.eye(3)

    # with intrinsic orientations, we post-multiply the rotation matrices
    if intrinsic:
        for idx, axis in enumerate(seq):
            result = result.dot(rot_mapping[axis](angles[idx]))
    # with extrinsic orientations, we pre-multiply the rotation matrices
    elif extrinsic:
        for idx, axis in enumerate(seq):
            result = rot_mapping[axis](angles[idx]).dot(result)

    return result


def from_quaternion(quat: Vector, normalized: bool = False):
    # consistent arguments
    quat = np_.asarray(quat)

    # normalize if needed
    if not normalized:
        quat = quat / np_.linalg.norm(quat)

    x = quat[0]
    y = quat[1]
    z = quat[2]
    w = quat[3]

    x2 = x * x
    y2 = y * y
    z2 = z * z
    w2 = w * w

    xy = x * y
    zw = z * w
    xz = x * z
    yw = y * w
    yz = y * z
    xw = x * w

    dcm = np_.empty((3, 3))

    dcm[0, 0] = x2 - y2 - z2 + w2
    dcm[1, 0] = 2 * (xy + zw)
    dcm[2, 0] = 2 * (xz - yw)

    dcm[0, 1] = 2 * (xy - zw)
    dcm[1, 1] = - x2 + y2 - z2 + w2
    dcm[2, 1] = 2 * (yz + xw)

    dcm[0, 2] = 2 * (xz + yw)
    dcm[1, 2] = 2 * (yz - xw)
    dcm[2, 2] = - x2 - y2 + z2 + w2

    return dcm


def steps(start: '_pose.Pose',
          end: '_pose.Pose',
          step: Union[Num, Vector]):
    # get an array
    step = np_.asarray(step)

    # convert scalar arrays into vectorial arrays
    if step.ndim == 0:
        step = np_.asarray([step])

    # [pos, rot] to [pos, pos, pos, rot, rot, rot]
    if step.size == 2:
        step = np_.hstack((
            np_.repeat(step[0], 3, axis=0),
            np_.repeat(step[1], 3, axis=0),
        ))

    # make sure the number of steps is 6 i.e., one per spatial degree of freedom
    if step.size != 6:
        step = np_.repeat(step, np_.ceil(6 / step.size))[0:6]

    # differences in position
    diff_pos = end.linear.position - start.linear.position

    # difference in orientation parametrization: note that we have to make
    # sure both poses are using the same sequence when getting their Euler
    # angles, which is why we have that `old_sequence` thing in there
    old_sequence = end.angular.sequence
    end.angular.sequence = start.angular.sequence
    diff_rot = end.angular.euler - start.angular.euler
    end.angular.sequence = old_sequence

    # delta in position to perform per step
    deltas = np_.hstack((diff_pos, diff_rot)) / step
    # set deltas to zero where no step is needed
    deltas[np_.isclose(step, 0)] = 0

    # how many iterations to perform per axis
    iterations = step * np_.logical_not(
        np_.hstack((np_.isclose(diff_pos, 0), np_.isclose(diff_rot, 0))))

    # TODO make creation of rotation matrix faster as `from_euler` seems to
    #  be a major bottleneck here
    # return the generator object
    return (_pose.Pose((
        start.linear.position + deltas[0:3] * a[0:3],
        from_euler(start.angular.sequence,
                   start.angular.euler + deltas[3:6] * a[3:6])
    )) for a in itertools.product(
        *(range(0, iterations[k] + 1) for k in range(0, 6))
    ))


def interval(pose: '_pose.Pose',
             boundaries: Union[Vector, Matrix],
             step: Union[Num, Vector] = 10):
    """

    Parameters
    ----------
    pose : Pose
    boundaries : iterable
        Boundaries around the pose to inspect. If given as 2-tuple i.e.,
        `[min, max]`, it is the minimum and maximum difference in all
        coordinates of the pose. If given as a 2-tuple of 2-tuples i.e.,
        `[[min, max], [min, max]]`, then `boundaries[0]` will be applied to all
        coordinates of the position and `boundaries[1]` will be applied to
        all coordinates of the orientation.
        If given as 6-tuple of 2-tuples i.e., `[[min, max], ..., [min,
        max]]`, then these boundaries will be applied to each coordinate
        separately.

    Returns
    -------

    """

    # we love working with numpy arrays
    boundaries = np_.asarray(boundaries)

    # case of [min, max]
    if boundaries.ndim == 1:
        boundaries = np_.repeat(boundaries[:, np_.newaxis], 6, axis=1)

    # case of [[min, max], [min, max]]
    if boundaries.ndim == 2 and boundaries.shape == (2, 2):
        boundaries = np_.hstack((
            np_.repeat(boundaries[0, :, np_.newaxis], 3, axis=1),  # position
            np_.repeat(boundaries[1, :, np_.newaxis], 3, axis=1),  # orientation
        ))

    # case of [[min, max], [min, max], ..., [min, max]]
    if boundaries.ndim == 2 and boundaries.shape == (6, 2):
        boundaries = boundaries.T

    # calculate start and end pose
    start = _pose.Pose(
        (
            pose.linear.position + boundaries[0, 0:3],
            from_euler(pose.angular.sequence,
                       pose.angular.euler + boundaries[0, 3:6])
        )
    )
    end = _pose.Pose(
        (
            pose.linear.position + boundaries[1, 0:3],
            from_euler(pose.angular.sequence,
                       pose.angular.euler + boundaries[1, 3:6])
        )
    )

    # now that we have a start and end pose, we will just pass down to the
    # steps generator
    return steps(start, end, step)


def translation(start: '_linear.Linear',
                end: '_linear.Linear',
                angular: Optional['_angular.Angular'] = None,
                step: Optional[Union[Num, Vector]] = None):
    """
    Generator for purely translational
    Parameters
    ----------
    start : Pose
        Start pose at which to start the translation-only pose generator
    end : Pose
        Final pose at which to end the translation-only pose generator
    angular : Matrix
        Fixed rotation matrix which to use at every pose. If not given,
        defaults to unit rotation matrix.
    step : Num | Vector | 3-tuple
        Number of discretization steps for the translation generator

    Returns
    -------

    """

    # by default, we will make 10 steps
    step = step if step else 10

    # ensure step has the right format (either (), (1,) or (3,))
    step = np_.asarray(step)
    if step.ndim == 0:
        step = np_.asarray([step])
    if step.size < 3:
        step = np_.repeat(step, 4 - step.size)[0:3]

    # no rotation matrix given, then take unity
    if angular is None:
        angular = _angular.Angular()

    # validate `step` is the right shape
    _validator.linalg.shape(step, (3,), 'step')

    # ensure both poses have the same rotation
    start.angular = angular
    end.angular = angular

    # return the steps iterator
    return steps(start, end, np_.pad(step, (0, 3)))


def orientation(start: '_angular.Angular',
                end: '_angular.Angular',
                position: Optional['_linear.Linear'] = None,
                step: Optional[Union[Num, Vector]] = None):
    """
    Create a generator of poses where only the orientation changes throughout
    the iteration

    Parameters
    ----------
    start : Matrix
        Initial rotation matrix given as
    end : Matrix
        Final rotation matrix.
    position : Pose
        Position at which to perform the rotation. If not given, defaults to
        [0.0, 0.0, 0.0]
    step : Num | Vector | 3-tuple
        Number of discretization steps for the orientation generator

    Returns
    -------
    generator
        A pose generator that loops over all poses defined in the orientation
        set of the given start and end rotation matrices. It is discretized
        in step steps per the three axes
    """

    # ensure step has the right format (either (), (1,) or (3,))
    step = np_.asarray(step)
    if step.ndim == 0:
        step = np_.asarray([step])
    if step.size < 3:
        step = np_.repeat(step, 4 - step.size)[0:3]

    # default position value
    if position is None:
        position = _linear.Linear()

    # validate step has the right shape
    _validator.linalg.rotation_matrix(step, (3,), 'step')

    # create start pose from the position pose given
    start = _pose.Pose(linear=position, angular=start)

    # create end pose from the position pose given
    end = _pose.Pose(linear=position, angular=end)

    # return the steps iterator
    return steps(start, end, np_.pad(step, (3, 0)))
