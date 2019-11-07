import numpy as np
import pytest

from cdpyr.analysis.kinematics.algorithm import Algorithm as Calculator
from cdpyr.motion import Pose
from cdpyr.robot import Robot


class StandardKinematicsTestSuite(object):

    def test_motion_pattern_1t(self,
                               robot_1t: Robot,
                               rand_pose_1t: Pose,
                               ik_standard: Calculator):
        # shift so we can copy code more easily from one test case to another
        rand_pose = rand_pose_1t

        res_backward = ik_standard.backward(robot_1t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_1t.kinematic_chains.with_platform(
                                       robot_1t.platforms[0]).frame_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_1t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            1, robot_1t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_1t.num_kinematic_chains, ))
        assert rand_pose.linear.position[0:1,
               np.newaxis] + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                   frame_anchor[0:1, :])

        res_forward = ik_standard.forward(robot_1t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_1t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            1, robot_1t.num_kinematic_chains)

    def test_motion_pattern_2t(self,
                               robot_2t: Robot,
                               rand_pose_2t: Pose,
                               ik_standard: Calculator):
        rand_pose = rand_pose_2t

        res_backward = ik_standard.backward(robot_2t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_2t.kinematic_chains.with_platform(
                                       robot_2t.platforms[0]).frame_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_2t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            2, robot_2t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_2t.num_kinematic_chains, ))
        assert rand_pose.linear.position[0:2, np.newaxis] \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                   frame_anchor[0:2, :])

        res_forward = ik_standard.forward(robot_2t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_2t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            2, robot_2t.num_kinematic_chains)

    def test_motion_pattern_3t(self,
                               robot_3t: Robot,
                               rand_pose_3t: Pose,
                               ik_standard: Calculator):
        rand_pose = rand_pose_3t

        res_backward = ik_standard.backward(robot_3t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_3t.kinematic_chains.with_platform(
                                       robot_3t.platforms[0]).frame_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_3t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot_3t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_3t.num_kinematic_chains, ))
        assert rand_pose.linear.position[0:3,
               np.newaxis] + res_backward.lengths * res_backward.directions == \
               pytest.approx(frame_anchor[0:3, :])

        res_forward = ik_standard.forward(robot_3t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_3t.num_kinematic_chains)

    def test_motion_pattern_1r2t(self,
                                 robot_1r2t: Robot,
                                 rand_pose_1r2t: Pose,
                                 ik_standard: Calculator):
        rand_pose = rand_pose_1r2t

        res_backward = ik_standard.backward(robot_1r2t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_1r2t.kinematic_chains.with_platform(
                                       robot_1r2t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_1r2t.kinematic_chains.with_platform(
                                          robot_1r2t.platforms[
                                              0]).platform_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_1r2t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            2, robot_1r2t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_1r2t.num_kinematic_chains, ))
        assert rand_pose.linear.position[0:2,
               np.newaxis] + rand_pose.angular.dcm[0:2, 0:2].dot(
            platform_anchor[0:2, :]) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                   frame_anchor[0:2, :])

        res_forward = ik_standard.forward(robot_1r2t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_1r2t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            2, robot_1r2t.num_kinematic_chains)

    def test_motion_pattern_2r3t(self,
                                 robot_2r3t: Robot,
                                 rand_pose_2r3t: Pose,
                                 ik_standard: Calculator):
        rand_pose = rand_pose_2r3t

        res_backward = ik_standard.backward(robot_2r3t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_2r3t.kinematic_chains.with_platform(
                                       robot_2r3t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_2r3t.kinematic_chains.with_platform(
                                          robot_2r3t.platforms[
                                              0]).platform_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_2r3t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot_2r3t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_2r3t.num_kinematic_chains, ))
        assert rand_pose.linear.position[:, np.newaxis] \
               + rand_pose.angular.dcm.dot(platform_anchor) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                   frame_anchor)

        res_forward = ik_standard.forward(robot_2r3t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_2r3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_2r3t.num_kinematic_chains)

    def test_motion_pattern_3r3t(self,
                                 robot_3r3t: Robot,
                                 rand_pose_3r3t: Pose,
                                 ik_standard: Calculator):
        rand_pose = rand_pose_3r3t

        res_backward = ik_standard.backward(robot_3r3t, rand_pose)

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_3r3t.kinematic_chains.with_platform(
                                       robot_3r3t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_3r3t.kinematic_chains.with_platform(
                                          robot_3r3t.platforms[
                                              0]).platform_anchor]).T

        assert res_backward.pose == rand_pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot_3r3t.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (
            3, robot_3r3t.num_kinematic_chains)
        assert np.linalg.norm(res_backward.directions, axis=0) == pytest.approx(
            np.ones(robot_3r3t.num_kinematic_chains, ))
        assert rand_pose.linear.position[:, np.newaxis] \
               + rand_pose.angular.dcm.dot(platform_anchor) \
               + res_backward.lengths * res_backward.directions == \
               pytest.approx(
                   frame_anchor)

        res_forward = ik_standard.forward(robot_3r3t, res_backward.joints)
        # print(rand_pose.linear.position, rel=1e-4, abs=1e-4)
        # print(rand_pose.angular.quaternion)

        assert res_forward.pose.linear.position == pytest.approx(
            rand_pose.linear.position, rel=1e-4, abs=1e-4)
        assert res_forward.pose.angular.quaternion == pytest.approx(rand_pose.angular.quaternion, rel=1e-4, abs=1e-4)
        # assert res_forward.pose.angular.dcm == pytest.approx(
        #     rand_pose.angular.dcm, rel=1e-4, abs=1e-6)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot_3r3t.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (
            3, robot_3r3t.num_kinematic_chains)


if __name__ == "__main__":
    pytest.main()
