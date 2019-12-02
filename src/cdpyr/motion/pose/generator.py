import itertools
from typing import AnyStr, Iterable, Optional, Tuple, Union

import numpy as np_

from cdpyr import validator as _validator
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def full(position: Tuple[Union[Num, Vector], Union[Num, Vector]],
         angle: Tuple[Union[Num, Vector], Union[Num, Vector]],
         sequence: str,
         steps: Union[
             Num, Tuple[Union[Num, Vector], Union[Num, Vector]]] = 10):
    # Default arguments for the steps
    steps = 5 if steps is None else steps

    # ensure both position values are numpy arrays
    position = [np_.asarray(x if isinstance(x, Iterable) else [x]) for x in
                position]
    # ensure both angle values are numpy arrays
    angle = [np_.asarray(x if isinstance(x, Iterable) else [x]) for x in angle]

    # now make sure both start and end position have the same size
    _validator.data.length(position[1], position[0].size, 'position[1]')
    # and make sure both start and end angles have the size given through the
    # sequence
    [_validator.data.length(a, len(sequence), f'angle[{idx}]') for idx, a in
     enumerate(angle)]

    # count values
    nums = (position[0].size, angle[0].size)

    # if steps is not an iterable object, we will make it one
    if not isinstance(steps, Iterable):
        steps = (steps, steps)

    # at this point, steps is either a 2-tuple of (steps[pos], steps[angle])
    # or it is a 2-tuple of ([steps[pos_0], ..., steps[pos_n]], [steps[
    # angle_0], ..., steps[angle_n]]) so let's check for that
    steps = [np_.asarray(
            step if isinstance(step, Iterable) else np_.repeat(step, num)) for
            num, step in zip(nums, steps)]

    # check steps has the right dimensions now, should be count ((Np, ), (Na, ))
    [_validator.data.length(step, nums[idx], f'steps[{idx}]') for idx, step in
     enumerate(steps)]

    # calculate the delta per step for each degree of freedom
    deltas = [(v[1] - v[0]) / step for v, step in zip((position, angle), steps)]
    # set deltas to zero where there is no step needed
    for idx in range(2):
        deltas[idx][np_.logical_or(np_.allclose(steps[idx], 0),
                                   np_.isnan(deltas[idx]))] = 0

    # at this point, we must ensure that the values for `position` are all
    # `(3,)` arrays
    position = [np_.pad(pos, (0, 3 - pos.size)) for pos in position]
    # from this follows, that we must also ensure that `steps[0]` now
    # contains 3 elements since the position now has three elements
    steps[0] = np_.pad(steps[0], (0, 3 - steps[0].size))
    deltas[0] = np_.pad(deltas[0], (0, 3 - deltas[0].size))

    # Finally, return the iterator object
    return (_pose.Pose(
            position[0] + deltas[0] * step[0:3],
            angular=_angular.Angular(
                    sequence=sequence,
                    euler=angle[0] + deltas[1] * step[3:])
    ) for step in
            itertools.product(*(range(k + 1) for k in itertools.chain(*steps))))


def translation(start: Union[Num, Vector],
                end: Union[Num, Vector],
                dcm: Optional[Matrix] = None,
                steps: Union[None, Num, Vector] = None):
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
    steps : Num | Vector | N-tuple
        Number of discretization steps from `start` to `end`. If given as
        number, will be applied to all dimensions of start, otherwise must
        match the size of `start`.

    Returns
    -------

    """

    # by default, we will make 10 steps
    steps = 10 if steps is None else steps

    # convert all into numpy arrays
    start = np_.asarray(start)
    end = np_.asarray(end)
    steps = np_.asarray(steps, dtype=np_.int)
    if start.ndim == 0:
        start = np_.asarray([start])
    if end.ndim == 0:
        end = np_.asarray([end])
    if steps.ndim == 0:
        steps = np_.asarray([steps], dtype=np_.int)

    # count the number of dimensions
    num_position = start.size

    # ensure `end` has the right size
    _validator.data.length(end, num_position, 'end')
    # if `step` is given with only one dimension, pad it to match the number
    # of dimensions
    if steps.size < num_position:
        steps = np_.repeat(steps, num_position - (steps.size - 1))
    # ensure `step` now has the right size
    _validator.data.length(steps, num_position, 'step')

    # no rotation matrix given, then take unity
    if dcm is None:
        dcm = np_.eye(3)
    _validator.linalg.rotation_matrix(dcm, 'dcm')

    # all data is validated, so make sure that both `start` and `end` are `(
    # 3,)`, otherwise `Pose` will complain
    start = np_.pad(start, (0, 3 - start.size))
    end = np_.pad(end, (0, 3 - end.size))
    steps = np_.repeat(steps, start.size - (steps.size - 1))[0:3]

    # calculate difference between `start` and `end` position
    diff = end - start
    # and delta per step
    delta = diff / steps
    # remove numeric artifacts and set to `0` where there must be no steps
    delta[np_.isclose(steps, 0)] = 0

    # how many iterations to perform per axis
    iterations = steps * np_.logical_not(np_.isclose(diff, 0))

    # return an iterator object
    return (_pose.Pose(start + delta * step, dcm) for step in
            itertools.product(*(range(k + 1) for k in iterations)))


def orientation(start: Union[Num, Vector],
                end: Union[Num, Vector],
                sequence: AnyStr,
                position: Optional[Vector] = None,
                steps: Union[None, Num, Vector] = None):
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
    steps : Num | Vector | N-tuple
        Number of discretization steps from `start` to `end`. If given as
        number, will be applied to all dimensions of start, otherwise must
        match the size of `start`.

    Returns
    -------

    """

    # by default, we will make 10 steps
    steps = 10 if steps is None else steps

    # convert all into numpy arrays
    start = np_.asarray(start)
    end = np_.asarray(end)
    steps = np_.asarray(steps, dtype=np_.int)
    if start.ndim == 0:
        start = np_.asarray([start])
    if end.ndim == 0:
        end = np_.asarray([end])
    if steps.ndim == 0:
        steps = np_.asarray([steps], dtype=np_.int)

    # count the number of dimensions
    num_euler = start.size

    # ensure sequence length matches the number of start euler angles
    _validator.data.length(sequence, num_euler, 'sequence')
    # ensure `end` has the right size
    _validator.data.length(end, num_euler, 'end')
    # if `step` is given with only one dimension, pad it to match the number
    # of dimensions
    if steps.size < num_euler:
        steps = np_.repeat(steps, num_euler - (steps.size - 1))
    # ensure `step` now has the right size
    _validator.data.length(steps, num_euler, 'step')

    # no rotation matrix given, then take unity
    if position is None:
        position = np_.asarray([0.0, 0.0, 0.0])

    # right-pad position with zeros so that `Pose` won't throw an error
    position = np_.pad(position, (0, 3 - position.size))

    # repeat step to match the amount of rotations to do
    steps = np_.repeat(steps, start.size - (steps.size - 1))[0:num_euler]

    # calculate difference between `start` and `end` position
    diff = end - start
    # and delta per step
    delta = diff / steps
    # remove numeric artifacts and set to `0` where there must be no steps
    delta[np_.isclose(steps, 0)] = 0

    # how many iterations to perform per axis
    iterations = steps * np_.logical_not(np_.isclose(diff, 0))

    # return an iterator object
    return (_pose.Pose(
            position,
            angular=_angular.Angular(
                    sequence=sequence,
                    euler=start + delta * step
            )) for step in
    itertools.product(*(range(k + 1) for k in iterations)))
