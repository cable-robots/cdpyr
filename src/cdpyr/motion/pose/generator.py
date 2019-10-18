import itertools
from typing import Optional, Union

import numpy as np_
from scipy.spatial import transform as _transform

from cdpyr import validator as _validator
from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Num, Vector


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
        _transform.Rotation.from_euler(start.angular.sequence,
                                       start.angular.euler
                                       + deltas[3:6]
                                       * a[3:6]
                                       ).as_dcm()
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
            _transform.Rotation.from_euler(pose.angular.sequence,
                                           pose.angular.euler + boundaries[0,
                                                                3:6]).as_dcm()
        )
    )
    end = _pose.Pose(
        (
            pose.linear.position + boundaries[1, 0:3],
            _transform.Rotation.from_euler(pose.angular.sequence,
                                           pose.angular.euler + boundaries[1,
                                                                3:6]).as_dcm()
        )
    )

    # now that we have a start and end pose, we will just pass down to the
    # steps generator
    return steps(start, end, step)
