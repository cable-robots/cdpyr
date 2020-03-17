import itertools
from typing import (
    AnyStr,
    Iterable,
    Union
)

import numpy as np
import pytest

from cdpyr.kinematics.transformation import angular
from cdpyr.motion import generator
from cdpyr.motion import pose
from cdpyr.typing import (
    Num,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorFullTestSuite(object):

    @pytest.mark.parametrize(
        ['position', 'angle', 'sequence', 'steps'],
        itertools.chain(
            (((0.0, 1.0), (-np.pi, np.pi), 'x', step) for step in
             (None, 3)),
            ((([0.0, 0.0], [1.0, 2.0]), ([-np.pi, np.pi], [np.pi, -np.pi]),
              'xy', step) for step in (None, 3, [3, 5])),
            ((([0.0, 0.0, 0.0], [1.0, 2.0, 3.0]),
              ([-np.pi, np.pi, -0.5 * np.pi], [np.pi, -np.pi, 0.5 * np.pi]),
              'xyz', step) for step in
             (None, 3, [3, 5], [[3, 5, 7], [7, 5, 3]]))
        )
    )
    def test_works_as_expected(self,
                               position: Vector,
                               angle: Vector,
                               sequence: AnyStr,
                               steps: Union[Num, Vector]):
        # get a pose generator
        actual_poses = generator.full(position, angle, sequence, steps)

        # Default arguments for the steps
        steps = 5 if steps is None else steps

        # ensure both position values are numpy arrays
        position = [np.asarray(x if isinstance(x, Iterable) else [x]) for x in
                    position]
        # ensure both angle values are numpy arrays
        angle = [np.asarray(x if isinstance(x, Iterable) else [x]) for x in
                 angle]

        # count values
        nums = (position[0].size, angle[0].size)

        # if steps is not an iterable object, we will make it one
        if not isinstance(steps, Iterable):
            steps = (steps, steps)

        # at this point, steps is either a 2-tuple of (steps[pos], steps[angle])
        # or it is a 2-tuple of ([steps[pos_0], ..., steps[pos_n]], [steps[
        # angle_0], ..., steps[angle_n]]) so let's check for that
        steps = [np.asarray(
            step if isinstance(step, Iterable) else np.repeat(step, num)) for
            num, step in zip(nums, steps)]

        # calculate the delta per step for each degree of freedom
        deltas = [(v[1] - v[0]) / step for v, step in
                  zip((position, angle), steps)]
        # set deltas to zero where there is no step needed
        for idx in range(2):
            deltas[idx][np.logical_or(np.allclose(steps[idx], 0),
                                      np.isnan(deltas[idx]))] = 0

        # at this point, we must ensure that the values for `position` are all
        # `(3,)` arrays
        position = [np.pad(pos, (0, 3 - pos.size)) for pos in position]
        # from this follows, that we must also ensure that `steps[0]` now
        # matches
        # the size of the positions
        steps[0] = np.pad(steps[0], (0, 3 - steps[0].size))
        deltas[0] = np.pad(deltas[0], (0, 3 - deltas[0].size))

        # Finally, return the iterator object
        expected_poses = (pose.Pose(
            position[0] + deltas[0] * step[0:3],
            angular=angular.Angular(
                sequence=sequence,
                euler=angle[0] + deltas[1] * step[3:])
        ) for step in
            itertools.product(*(range(k + 1) for k in itertools.chain(*steps))))

        for actual, expected in zip(actual_poses, expected_poses):
            assert actual == expected

    @pytest.mark.parametrize(
        ['position', 'angle', 'sequence', 'steps'],
        itertools.chain(
            (((0.0, 1.0), (-np.pi, np.pi), 'xy', step) for step in
             (None, 3)),
            ((([0.0, 0.0], [1.0, 2.0]), ([-np.pi, np.pi], [np.pi, -np.pi]),
              'xzy', step) for step in (None, 3, [3, 5])),
            ((([0.0, 0.0, 0.0], [1.0, 2.0, 3.0]),
              ([-np.pi, np.pi, -0.5 * np.pi], [np.pi, -np.pi, 0.5 * np.pi]),
              'xy', step) for step in
             (None, 3, [3, 5], [[3, 5, 7], [7, 5, 3]]))
        )
    )
    def test_failes_because_of_wrong_arguments(self,
                               position: Vector,
                               angle: Vector,
                               sequence: AnyStr,
                               steps: Union[Num, Vector]):
        with pytest.raises(ValueError):
            generator.full(position, angle, sequence, steps)


if __name__ == "__main__":
    pytest.main()
