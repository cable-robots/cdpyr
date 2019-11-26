import itertools
from typing import (
    AnyStr,
    Optional,
    Union
)

import numpy as np_

from cdpyr import validator as _validator
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import (
    Matrix,
    Num,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def full(start_position: Union[Num, Vector],
         end_position: Union[Num, Vector],
         start_euler: Union[Num, Vector],
         end_euler: Union[Num, Vector],
         sequence: str,
         step: Union[None, Num, Vector] = None):
    # by default, we will make 10 steps
    step = step if step else 10

    # convert all into numpy arrays
    start_position = np_.asarray(start_position)
    end_position = np_.asarray(end_position)
    start_euler = np_.asarray(start_euler)
    end_euler = np_.asarray(end_euler)
    step = np_.asarray(step, dtype=np_.int)
    if start_position.ndim == 0:
        start_position = np_.asarray([start_position])
    if end_position.ndim == 0:
        end_position = np_.asarray([end_position])
    if start_euler.ndim == 0:
        start_euler = np_.asarray([start_euler])
    if end_euler.ndim == 0:
        end_euler = np_.asarray([end_euler])
    if step.ndim == 0:
        step = np_.asarray([step], dtype=np_.int)

    # count coordinates of both position and orientation
    num_coordinates_position = start_position.size
    num_coordinates_euler = start_euler.size
    num_coordinates = num_coordinates_position + num_coordinates_euler

    # check start and end position have same size
    _validator.data.length(end_position, num_coordinates_position,
                           'end_position')
    # check the sequence length matches the length of the start euler angles
    _validator.data.length(sequence, num_coordinates_euler, 'sequence')
    # check start and end euler have same size
    _validator.data.length(end_euler, num_coordinates_euler, 'end_euler')

    # if `step` is given with only one dimension, pad it to match the number
    # of dimensions
    if step.size < num_coordinates:
        step = np_.repeat(step, num_coordinates - (step.size - 1))
        # step = np_.repeat(step, (0, num_coordinates - step.size))
    # ensure `step` now has the right size
    _validator.data.length(step, num_coordinates, 'step')

    # all data is validated, so make sure that both `start` and `end` are `(
    # 3,)`, otherwise `Pose` will complain
    start_position = np_.pad(start_position, (0, 3 - start_position.size))
    end_position = np_.pad(end_position, (0, 3 - end_position.size))
    step = np_.repeat(step, 3 + num_coordinates_euler - (step.size - 1))[0:3 + num_coordinates_euler]

    # calculate differences in position and euler angles
    diff_position = end_position - start_position
    diff_euler = end_euler - start_euler
    # and delta per step
    delta_position = diff_position / step[0:3]
    delta_euler = diff_euler / step[3:]
    # remove numeric artifacts and set to `0` where there must be no steps
    delta_position[np_.isclose(step[0:3], 0)] = 0
    delta_euler[np_.isclose(step[3:], 0)] = 0

    # how many iterations to perform per axis
    iterations = step * np_.logical_not(
        np_.hstack((np_.isclose(diff_position, 0), np_.isclose(diff_euler, 0))))

    # return an iterator object
    return (_pose.Pose(
        start_position + delta_position * step[0:3],
        angular=_angular.Angular(
            sequence=sequence,
            euler=start_euler + delta_euler * step[3:6])
    ) for step in itertools.product(*(range(k + 1) for k in iterations)))


def translation(start: Union[Num, Vector],
                end: Union[Num, Vector],
                dcm: Optional[Matrix] = None,
                step: Union[None, Num, Vector] = None):
    """
    Generator for purely translational changing poses
    Parameters
    ----------
    start : Num | Vector
        Start position at which the translation-only pose generator should
        start. Can be of size up to 3.
    end : Num | Vector
        Start position at which the translation-only pose generator should
        end. Must be the same size as `start`.
    dcm : Matrix | Angular
        Fixed rotation matrix which to use at every pose. If not given,
        defaults to unit rotation matrix.
    step : Num | Vector | N-tuple
        Number of discretization steps from `start` to `end`. If given as
        number, will be applied to all dimensions of start, otherwise must
        match the size of `start`.

    Returns
    -------

    """

    # by default, we will make 10 steps
    step = step if step else 10

    # convert all into numpy arrays
    start = np_.asarray(start)
    end = np_.asarray(end)
    step = np_.asarray(step, dtype=np_.int)
    if start.ndim == 0:
        start = np_.asarray([start])
    if end.ndim == 0:
        end = np_.asarray([end])
    if step.ndim == 0:
        step = np_.asarray([step], dtype=np_.int)

    # count the number of dimensions
    num_coordinates = start.size

    # ensure `end` has the right size
    _validator.data.length(end, num_coordinates, 'end')
    # if `step` is given with only one dimension, pad it to match the number
    # of dimensions
    if step.size < num_coordinates:
        step = np_.repeat(step, num_coordinates - (step.size - 1))
        # step = np_.repeat(step, (0, num_coordinates - step.size))
    # ensure `step` now has the right size
    _validator.data.length(step, num_coordinates, 'step')

    # no rotation matrix given, then take unity
    if dcm is None:
        dcm = np_.eye(3)
    _validator.linalg.rotation_matrix(dcm, 'dcm')

    # all data is validated, so make sure that both `start` and `end` are `(
    # 3,)`, otherwise `Pose` will complain
    start = np_.pad(start, (0, 3 - start.size))
    end = np_.pad(end, (0, 3 - end.size))
    step = np_.repeat(step, start.size - (step.size - 1))[0:3]

    # calculate difference between `start` and `end` position
    diff = end - start
    # and delta per step
    delta = diff / step
    # remove numeric artifacts and set to `0` where there must be no steps
    delta[np_.isclose(step, 0)] = 0

    # how many iterations to perform per axis
    iterations = step * np_.logical_not(np_.isclose(diff, 0))

    # return an iterator object
    return (_pose.Pose(start + delta * step, dcm) for step in
            itertools.product(*(range(k + 1) for k in iterations)))


def orientation(start: Union[Num, Vector],
                end: Union[Num, Vector],
                sequence: AnyStr,
                position: Optional[Vector] = None,
                step: Union[None, Num, Vector] = None):
    """
    Generator for purely orientational changing poses
    Parameters
    ----------
    start : Num | Vector
        Orientation given in Euler angles at which the orientation-only
        pose generator should start.
    end : Num | Vector
        Orientation given in Euler angles at which the orientation-only
        pose generator should end. Must be the same size as `start`.
    sequence : AnyStr
        Sequence of Euler orientations used to reconstruct the orientation
        matrix. Can be any valid combination of intrinsic `(x, y, z)` or
        extrinsic `(X, Y, Z)`. Number of rotations must match the number of
        start Euler angles.
    position : Num | Vector
        Fix position vector at which the orientational poses should be
        applied. Any non `(3,)` vector or scalar will be padded up to
        dimension `(3,)`.
    step : Num | Vector | N-tuple
        Number of discretization steps from `start` to `end`. If given as
        number, will be applied to all dimensions of start, otherwise must
        match the size of `start`.

    Returns
    -------

    """

    # by default, we will make 10 steps
    step = step if step else 10

    # convert all into numpy arrays
    start = np_.asarray(start)
    end = np_.asarray(end)
    step = np_.asarray(step, dtype=np_.int)
    if start.ndim == 0:
        start = np_.asarray([start])
    if end.ndim == 0:
        end = np_.asarray([end])
    if step.ndim == 0:
        step = np_.asarray([step], dtype=np_.int)

    # count the number of dimensions
    num_coordinates = start.size

    # ensure sequence length matches the number of start euler angles
    _validator.data.length(sequence, num_coordinates, 'sequence')
    # ensure `end` has the right size
    _validator.data.length(end, num_coordinates, 'end')
    # if `step` is given with only one dimension, pad it to match the number
    # of dimensions
    if step.size < num_coordinates:
        step = np_.repeat(step, num_coordinates - (step.size - 1))
    # ensure `step` now has the right size
    _validator.data.length(step, num_coordinates, 'step')

    # no rotation matrix given, then take unity
    if position is None:
        position = np_.asarray([0.0, 0.0, 0.0])

    # right-pad position with zeros so that `Pose` won't throw an error
    position = np_.pad(position, (0, 3 - position.size))

    # repeat step to match the amount of rotations to do
    step = np_.repeat(step, start.size - (step.size - 1))[0:num_coordinates]

    # calculate difference between `start` and `end` position
    diff = end - start
    # and delta per step
    delta = diff / step
    # remove numeric artifacts and set to `0` where there must be no steps
    delta[np_.isclose(step, 0)] = 0

    # how many iterations to perform per axis
    iterations = step * np_.logical_not(np_.isclose(diff, 0))

    # return an iterator object
    return (_pose.Pose(
        position,
        angular=_angular.Angular(
            sequence=sequence,
            euler=start + delta * step
        )) for step in itertools.product(*(range(k + 1) for k in iterations)))
