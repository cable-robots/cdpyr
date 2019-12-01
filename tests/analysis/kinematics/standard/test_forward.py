import pytest

from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot


class StandardKinematicsForwardTestSuite(object):

    def test_motion_pattern_1t(self,
                               robot_1t: Robot,
                               rand_pose_1t: Pose,
                               ik_standard: StandardKinematics):
        # shift so we can copy code more easily from one test case to another
        rand_pose = rand_pose_1t

        res_backward = ik_standard.backward(robot_1t, rand_pose)
        res_forward = ik_standard.forward(robot_1t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_1t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            1, robot_1t.num_kinematic_chains)

    def test_motion_pattern_2t(self,
                               robot_2t: Robot,
                               rand_pose_2t: Pose,
                               ik_standard: StandardKinematics):
        rand_pose = rand_pose_2t

        res_backward = ik_standard.backward(robot_2t, rand_pose)
        res_forward = ik_standard.forward(robot_2t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_2t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            2, robot_2t.num_kinematic_chains)

    def test_motion_pattern_3t(self,
                               robot_3t: Robot,
                               rand_pose_3t: Pose,
                               ik_standard: StandardKinematics):
        rand_pose = rand_pose_3t

        res_backward = ik_standard.backward(robot_3t, rand_pose)
        res_forward = ik_standard.forward(robot_3t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_3t.num_kinematic_chains)

    def test_motion_pattern_1r2t(self,
                                 robot_1r2t: Robot,
                                 rand_pose_1r2t: Pose,
                                 ik_standard: StandardKinematics):
        rand_pose = rand_pose_1r2t

        res_backward = ik_standard.backward(robot_1r2t, rand_pose)
        res_forward = ik_standard.forward(robot_1r2t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_1r2t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            2, robot_1r2t.num_kinematic_chains)

    def test_motion_pattern_2r3t(self,
                                 robot_2r3t: Robot,
                                 rand_pose_2r3t: Pose,
                                 ik_standard: StandardKinematics):
        rand_pose = rand_pose_2r3t

        res_backward = ik_standard.backward(robot_2r3t, rand_pose)
        res_forward = ik_standard.forward(robot_2r3t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_2r3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_2r3t.num_kinematic_chains)

    def test_motion_pattern_3r3t(self,
                                 robot_3r3t: Robot,
                                 rand_pose_3r3t: Pose,
                                 ik_standard: StandardKinematics):
        rand_pose = rand_pose_3r3t

        res_backward = ik_standard.backward(robot_3r3t, rand_pose)
        res_forward = ik_standard.forward(robot_3r3t, res_backward.joints)

        assert res_forward.pose.linear.position == pytest.approx(
                rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(
                rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_3r3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_3r3t.num_kinematic_chains)


if __name__ == "__main__":
    pytest.main()
