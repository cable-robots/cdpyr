import pytest

from cdpyr.analysis.criterion import Interference
from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.kinematics.transformation import Angular
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot


class ClosedFormForceDistributionTestSuite(object):

    def test_something(self,
                       ik_standard: StandardKinematics,
                       robot_3r3t: Robot,
                       zero_pose: Pose):
        # make criterion
        criterion = Interference(ik_standard)

        zero_pose.angular = Angular.rotation_z(180, True)

        robot = robot_3r3t
        pose = zero_pose

        criterion.evaluate(robot, pose)


if __name__ == "__main__":
    pytest.main()
