import itertools
from typing import (
    AnyStr,
    Iterable,
    Union
)

import numpy as np
import pytest

from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import (
    generator_new as generator,
    pose as _pose
)
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
             (None, 11)),
            ((([0.0, 0.0], [1.0, 2.0]), ([-np.pi, np.pi], [np.pi, -np.pi]),
              'xy', step) for step in (None, 11, [11, 9])),
            ((([0.0, 0.0, 0.0], [1.0, 2.0, 3.0]),
              ([-np.pi, np.pi, -0.5 * np.pi], [np.pi, -np.pi, 0.5 * np.pi]),
              'xyz', step) for step in
             (None, 11, [11, 9], [[11, 9, 7], [7, 9, 11]]))
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
        steps = 10 if steps is None else steps

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
        expected_poses = (_pose.Pose(
            position[0] + deltas[0] * step[0:3],
            angular=_angular.Angular(
                sequence=sequence,
                euler=angle[0] + deltas[1] * step[3:])
        ) for step in
            itertools.product(*(range(k + 1) for k in itertools.chain(*steps))))

        for actual_pose, expected_pose in zip(actual_poses, expected_poses):
            assert actual_pose.linear.position == pytest.approx(
                expected_pose.linear.position)
            assert actual_pose.angular.dcm == pytest.approx(
                expected_pose.angular.dcm)

    # @pytest.mark.parametrize(
    #     ['start_position', 'end_position', 'start_euler', 'end_euler',
    #      'sequence', 'steps'],
    #     [
    #         (
    #             0.0,
    #             1.0,
    #             0.0,
    #             np.pi,
    #             'x',
    #             [25, 25, 25]
    #         ),
    #         (
    #             [0.0, 0.0],
    #             [1.0, 2.0],
    #             [0.0, 0.0],
    #             [-np.pi, np.pi],
    #             'xy',
    #             [25, 25]
    #         ),
    #         (
    #             [0.0, 0.0, 0.0],
    #             [1.0, 2.0, 3.0],
    #             [0.0, 0.0, 0.0],
    #             [-np.pi, np.pi, 1.5 * np.pi],
    #             'xyz',
    #             [25, 25]
    #         ),
    #     ]
    # )
    # def test_fails_because_of_wrong_steps_count(self,
    #                                             start_position: Vector,
    #                                             end_position: Vector,
    #                                             start_euler: Vector,
    #                                             end_euler: Vector,
    #                                             sequence: AnyStr,
    #                                             steps: Union[Num, Vector]):
    #     with pytest.raises(ValueError):
    #         generator.full(start_position, end_position, start_euler,
    #         end_euler,
    #                        sequence, steps)


if __name__ == "__main__":
    pytest.main()
