import numpy as np
import pytest
from scipy.spatial.transform import Rotation

import cdpyr


class StepsPoseGeneratorTestSuite(object):

    def test_steps_with_two_steps_on_one_change_in_position(self):
        pose_start = cdpyr.motion.Pose((
            (-0.0, -0.0, -1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (+0.0, +0.0, +1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 3
        assert poses[0].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [0, 0, 2, 0, 0, 0])

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 3
        assert poses[0].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))

    def test_steps_with_two_steps_on_two_changes_in_position(self):
        pose_start = cdpyr.motion.Pose((
            (-0.0, -1.0, -1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (+0.0, +1.0, +1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 9
        assert poses[0].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, +1.0)))
        assert poses[3].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[4].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[5].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))
        assert poses[6].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, -1.0)))
        assert poses[7].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, 0.0)))
        assert poses[8].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, +1.0)))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [0, 2, 2, 0, 0, 0])

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 9
        assert poses[0].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, +1.0)))
        assert poses[3].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[4].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[5].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))
        assert poses[6].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, -1.0)))
        assert poses[7].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, 0.0)))
        assert poses[8].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, +1.0)))

    def test_steps_with_two_steps_on_three_changes_in_position(self):
        pose_start = cdpyr.motion.Pose((
            (-1.0, -1.0, -1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (+1.0, +1.0, +1.0),
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 27
        assert poses[0].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, +1.0)))
        assert poses[3].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, -1.0)))
        assert poses[4].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, 0.0)))
        assert poses[5].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, +1.0)))
        assert poses[6].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, -1.0)))
        assert poses[7].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, 0.0)))
        assert poses[8].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, +1.0)))
        assert poses[9].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, -1.0)))
        assert poses[10].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, 0.0)))
        assert poses[11].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, +1.0)))
        assert poses[12].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[13].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[14].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))
        assert poses[15].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, -1.0)))
        assert poses[16].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, 0.0)))
        assert poses[17].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, +1.0)))
        assert poses[18].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, -1.0)))
        assert poses[19].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, 0.0)))
        assert poses[20].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, +1.0)))
        assert poses[21].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, -1.0)))
        assert poses[22].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, 0.0)))
        assert poses[23].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, +1.0)))
        assert poses[24].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, -1.0)))
        assert poses[25].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, 0.0)))
        assert poses[26].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, +1.0)))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [2, 2, 2, 0, 0, 0])

        # convert the generator into a list
        poses = list(pose_generator)

        # assertion
        assert len(poses) == 27
        assert poses[0].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, -1.0)))
        assert poses[1].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, 0.0)))
        assert poses[2].linear.position == pytest.approx(
            np.asarray((-1.0, -1.0, +1.0)))
        assert poses[3].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, -1.0)))
        assert poses[4].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, 0.0)))
        assert poses[5].linear.position == pytest.approx(
            np.asarray((-1.0, 0.0, +1.0)))
        assert poses[6].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, -1.0)))
        assert poses[7].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, 0.0)))
        assert poses[8].linear.position == pytest.approx(
            np.asarray((-1.0, 1.0, +1.0)))
        assert poses[9].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, -1.0)))
        assert poses[10].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, 0.0)))
        assert poses[11].linear.position == pytest.approx(
            np.asarray((0.0, -1.0, +1.0)))
        assert poses[12].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, -1.0)))
        assert poses[13].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, 0.0)))
        assert poses[14].linear.position == pytest.approx(
            np.asarray((0.0, 0.0, +1.0)))
        assert poses[15].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, -1.0)))
        assert poses[16].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, 0.0)))
        assert poses[17].linear.position == pytest.approx(
            np.asarray((0.0, 1.0, +1.0)))
        assert poses[18].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, -1.0)))
        assert poses[19].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, 0.0)))
        assert poses[20].linear.position == pytest.approx(
            np.asarray((+1.0, -1.0, +1.0)))
        assert poses[21].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, -1.0)))
        assert poses[22].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, 0.0)))
        assert poses[23].linear.position == pytest.approx(
            np.asarray((+1.0, 0.0, +1.0)))
        assert poses[24].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, -1.0)))
        assert poses[25].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, 0.0)))
        assert poses[26].linear.position == pytest.approx(
            np.asarray((+1.0, 1.0, +1.0)))

    def test_steps_with_two_steps_on_one_change_in_orientation(self):
        pose_start = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('z', -45, degrees=True).as_dcm()
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('z', 45, degrees=True).as_dcm()
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 3
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('z', -45, degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('z', 0, degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('z', +45, degrees=True).as_dcm())

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [0, 0, 0, 0, 0, 2])

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 3
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('z', -45, degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('z', 0, degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('z', +45, degrees=True).as_dcm())

    def test_steps_with_two_steps_on_two_changes_in_orientation(self):
        pose_start = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('xy', [-45, -45], degrees=True).as_dcm()
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('xy', [45, 45], degrees=True).as_dcm()
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 9
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, -45], degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, 0], degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, +45], degrees=True).as_dcm())
        assert poses[3].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, -45], degrees=True).as_dcm())
        assert poses[4].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, 0], degrees=True).as_dcm())
        assert poses[5].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, +45], degrees=True).as_dcm())
        assert poses[6].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, -45], degrees=True).as_dcm())
        assert poses[7].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, 0], degrees=True).as_dcm())
        assert poses[8].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, +45], degrees=True).as_dcm())

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [0, 0, 0, 2, 2, 0])

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 9
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, -45], degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, 0], degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [-45, +45], degrees=True).as_dcm())
        assert poses[3].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, -45], degrees=True).as_dcm())
        assert poses[4].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, 0], degrees=True).as_dcm())
        assert poses[5].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [0, +45], degrees=True).as_dcm())
        assert poses[6].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, -45], degrees=True).as_dcm())
        assert poses[7].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, 0], degrees=True).as_dcm())
        assert poses[8].angular.dcm == pytest.approx(
            Rotation.from_euler('xy', [+45, +45], degrees=True).as_dcm())

    def test_steps_with_two_steps_on_three_changes_in_orientation(self):
        pose_start = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('xyz', [-45, -45, -45],
                                    degrees=True).as_dcm()
            )
        ))

        pose_end = cdpyr.motion.Pose((
            (0.0, 0.0, 0.0),
            (
                Rotation.from_euler('xyz', [+45, +45, +45],
                                    degrees=True).as_dcm()
            )
        ))

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end, 2)

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 27
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, -45], degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, 0], degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, +45], degrees=True).as_dcm())
        assert poses[3].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, -45], degrees=True).as_dcm())
        assert poses[4].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, 0], degrees=True).as_dcm())
        assert poses[5].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, +45], degrees=True).as_dcm())
        assert poses[6].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, -45], degrees=True).as_dcm())
        assert poses[7].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, 0], degrees=True).as_dcm())
        assert poses[8].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, +45], degrees=True).as_dcm())

        assert poses[9].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, -45], degrees=True).as_dcm())
        assert poses[10].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, 0], degrees=True).as_dcm())
        assert poses[11].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, +45], degrees=True).as_dcm())
        assert poses[12].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, -45], degrees=True).as_dcm())
        assert poses[13].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, 0], degrees=True).as_dcm())
        assert poses[14].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, +45], degrees=True).as_dcm())
        assert poses[15].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, -45], degrees=True).as_dcm())
        assert poses[16].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, 0], degrees=True).as_dcm())
        assert poses[17].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, +45], degrees=True).as_dcm())

        assert poses[18].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, -45], degrees=True).as_dcm())
        assert poses[19].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, 0], degrees=True).as_dcm())
        assert poses[20].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, +45], degrees=True).as_dcm())
        assert poses[21].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, -45], degrees=True).as_dcm())
        assert poses[22].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, 0], degrees=True).as_dcm())
        assert poses[23].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, +45], degrees=True).as_dcm())
        assert poses[24].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, -45], degrees=True).as_dcm())
        assert poses[25].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, 0], degrees=True).as_dcm())
        assert poses[26].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, +45], degrees=True).as_dcm())

        # create a generator object
        pose_generator = cdpyr.motion.generator.steps(pose_start, pose_end,
                                                      [0, 0, 0, 2, 2, 2])

        # convert the generator into a list
        poses = list(pose_generator)
        print(pose_start.angular.sequence)

        # assertion
        assert len(poses) == 27
        assert poses[0].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, -45], degrees=True).as_dcm())
        assert poses[1].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, 0], degrees=True).as_dcm())
        assert poses[2].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, -45, +45], degrees=True).as_dcm())
        assert poses[3].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, -45], degrees=True).as_dcm())
        assert poses[4].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, 0], degrees=True).as_dcm())
        assert poses[5].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, 0, +45], degrees=True).as_dcm())
        assert poses[6].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, -45], degrees=True).as_dcm())
        assert poses[7].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, 0], degrees=True).as_dcm())
        assert poses[8].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [-45, +45, +45], degrees=True).as_dcm())

        assert poses[9].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, -45], degrees=True).as_dcm())
        assert poses[10].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, 0], degrees=True).as_dcm())
        assert poses[11].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, -45, +45], degrees=True).as_dcm())
        assert poses[12].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, -45], degrees=True).as_dcm())
        assert poses[13].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, 0], degrees=True).as_dcm())
        assert poses[14].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, 0, +45], degrees=True).as_dcm())
        assert poses[15].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, -45], degrees=True).as_dcm())
        assert poses[16].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, 0], degrees=True).as_dcm())
        assert poses[17].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+0, +45, +45], degrees=True).as_dcm())

        assert poses[18].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, -45], degrees=True).as_dcm())
        assert poses[19].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, 0], degrees=True).as_dcm())
        assert poses[20].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, -45, +45], degrees=True).as_dcm())
        assert poses[21].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, -45], degrees=True).as_dcm())
        assert poses[22].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, 0], degrees=True).as_dcm())
        assert poses[23].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, 0, +45], degrees=True).as_dcm())
        assert poses[24].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, -45], degrees=True).as_dcm())
        assert poses[25].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, 0], degrees=True).as_dcm())
        assert poses[26].angular.dcm == pytest.approx(
            Rotation.from_euler('xyz', [+45, +45, +45], degrees=True).as_dcm())


if __name__ == "__main__":
    pytest.main()
