import numpy as np
import pytest

from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot


class StandardKinematicsBackwardTestSuite(object):

    def test_motion_pattern_1t(self,
                               robot_1t: Robot,
                               rand_pose_1t: Pose,
                               ik_standard: StandardKinematics):
        robot = robot_1t
        pose = rand_pose_1t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            1, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[0:1,
               np.newaxis] + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                       frame_anchor[0:1, :])

    def test_motion_pattern_2t(self,
                               robot_2t: Robot,
                               rand_pose_2t: Pose,
                               ik_standard: StandardKinematics):
        robot = robot_2t
        pose = rand_pose_2t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            2, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[0:2, np.newaxis] \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                       frame_anchor[0:2, :])

    def test_motion_pattern_3t(self,
                               robot_3t: Robot,
                               rand_pose_3t: Pose,
                               ik_standard: StandardKinematics):
        robot = robot_3t
        pose = rand_pose_3t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[0:3,
               np.newaxis] + res_backward.lengths * res_backward.directions == \
               pytest.approx(frame_anchor[0:3, :])

    def test_motion_pattern_1r2t(self,
                                 robot_1r2t: Robot,
                                 rand_pose_1r2t: Pose,
                                 ik_standard: StandardKinematics):
        robot = robot_1r2t
        pose = rand_pose_1r2t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T
        platform_anchor = np.asarray([robot.platforms[platform_index].anchors[anchor_index].linear.position for anchor_index in kcs.platform_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            2, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[0:2,
               np.newaxis] + pose.angular.dcm[0:2, 0:2].dot(
                platform_anchor[0:2, :]) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                       frame_anchor[0:2, :])

    def test_motion_pattern_2r3t(self,
                                 robot_2r3t: Robot,
                                 rand_pose_2r3t: Pose,
                                 ik_standard: StandardKinematics):
        robot = robot_2r3t
        pose = rand_pose_2r3t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T
        platform_anchor = np.asarray([robot.platforms[platform_index].anchors[anchor_index].linear.position for anchor_index in kcs.platform_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[:, np.newaxis] \
               + pose.angular.dcm.dot(platform_anchor) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                       frame_anchor)

    def test_motion_pattern_3r3t(self,
                                 robot_3r3t: Robot,
                                 rand_pose_3r3t: Pose,
                                 ik_standard: StandardKinematics):
        robot = robot_3r3t
        pose = rand_pose_3r3t

        # solve the inverse kinematics
        res_backward = ik_standard.backward(robot, pose)

        # platform index (to fake the loop over all platforms)
        platform_index = 0

        # right order of frame and platform anchors
        kcs = robot.kinematic_chains.with_platform(platform_index)
        frame_anchor = np.asarray([robot.frame.anchors[anchor_index].linear.position for anchor_index in kcs.frame_anchor]).T
        platform_anchor = np.asarray([robot.platforms[platform_index].anchors[anchor_index].linear.position for anchor_index in kcs.platform_anchor]).T

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
                np.ones(robot.num_kinematic_chains, ))
        assert pose.linear.position[:, np.newaxis] \
               + pose.angular.dcm.dot(platform_anchor) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                       frame_anchor)


if __name__ == "__main__":
    pytest.main()
