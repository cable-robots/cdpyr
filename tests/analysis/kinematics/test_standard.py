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
        result = ik_standard.backward(robot_1t, rand_pose_1t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_1t.kinematic_chains.with_platform(
                                       robot_1t.platforms[0]).frame_anchor]).T

        assert result.pose == rand_pose_1t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_1t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (1, robot_1t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_1t.num_kinematic_chains, ))
        assert rand_pose_1t.linear.position[0:1,
               np.newaxis] + result.lengths * result.directions == \
               pytest.approx(
                   frame_anchor[0:1, :])

    def test_motion_pattern_2t(self,
                               robot_2t: Robot,
                               rand_pose_2t: Pose,
                               ik_standard: Calculator):
        result = ik_standard.backward(robot_2t, rand_pose_2t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_2t.kinematic_chains.with_platform(
                                       robot_2t.platforms[0]).frame_anchor]).T

        assert result.pose == rand_pose_2t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_2t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (2, robot_2t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_2t.num_kinematic_chains, ))
        assert rand_pose_2t.linear.position[0:2, np.newaxis] \
               + result.lengths * result.directions == pytest.approx(
            frame_anchor[0:2, :])

    def test_motion_pattern_3t(self,
                               robot_3t: Robot,
                               rand_pose_3t: Pose,
                               ik_standard: Calculator):
        result = ik_standard.backward(robot_3t, rand_pose_3t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_3t.kinematic_chains.with_platform(
                                       robot_3t.platforms[0]).frame_anchor]).T

        assert result.pose == rand_pose_3t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_3t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (3, robot_3t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_3t.num_kinematic_chains, ))
        assert rand_pose_3t.linear.position[0:3,
               np.newaxis] + result.lengths * result.directions == \
               pytest.approx(frame_anchor[0:3, :])

    def test_motion_pattern_1r2t(self,
                                 robot_1r2t: Robot,
                                 rand_pose_1r2t: Pose,
                                 ik_standard: Calculator):
        result = ik_standard.backward(robot_1r2t, rand_pose_1r2t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_1r2t.kinematic_chains.with_platform(
                                       robot_1r2t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_1r2t.kinematic_chains.with_platform(
                                          robot_1r2t.platforms[
                                              0]).platform_anchor]).T

        assert result.pose == rand_pose_1r2t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_1r2t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (2, robot_1r2t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_1r2t.num_kinematic_chains, ))
        assert rand_pose_1r2t.linear.position[0:2,
               np.newaxis] + rand_pose_1r2t.angular.dcm[0:2, 0:2].dot(
            platform_anchor[0:2, :]) \
               + result.lengths * result.directions == pytest.approx(
            frame_anchor[0:2, :])

    def test_motion_pattern_2r3t(self,
                                 robot_2r3t: Robot,
                                 rand_pose_2r3t: Pose,
                                 ik_standard: Calculator):
        result = ik_standard.backward(robot_2r3t, rand_pose_2r3t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_2r3t.kinematic_chains.with_platform(
                                       robot_2r3t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_2r3t.kinematic_chains.with_platform(
                                          robot_2r3t.platforms[
                                              0]).platform_anchor]).T

        assert result.pose == rand_pose_2r3t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_2r3t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (3, robot_2r3t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_2r3t.num_kinematic_chains, ))
        assert rand_pose_2r3t.linear.position[:, np.newaxis] \
               + rand_pose_2r3t.angular.dcm.dot(platform_anchor) \
               + result.lengths * result.directions == pytest.approx(
            frame_anchor)

    def test_motion_pattern_3r3t(self,
                                 robot_3r3t: Robot,
                                 rand_pose_3r3t: Pose,
                                 ik_standard: Calculator):
        result = ik_standard.backward(robot_3r3t, rand_pose_3r3t)

        # TODO implement the test for `forward`, too

        # right order of frame and platform anchors
        frame_anchor = np.asarray([anchor.position for anchor in
                                   robot_3r3t.kinematic_chains.with_platform(
                                       robot_3r3t.platforms[0]).frame_anchor]).T
        platform_anchor = np.asarray([anchor.position for anchor in
                                      robot_3r3t.kinematic_chains.with_platform(
                                          robot_3r3t.platforms[
                                              0]).platform_anchor]).T

        assert result.pose == rand_pose_3r3t
        assert result.lengths.ndim == 1
        assert result.lengths.shape == (robot_3r3t.num_kinematic_chains,)
        assert (0 <= result.lengths).all()
        assert result.directions.shape == (3, robot_3r3t.num_kinematic_chains)
        assert np.linalg.norm(result.directions, axis=0) == pytest.approx(
            np.ones(robot_3r3t.num_kinematic_chains, ))
        assert rand_pose_3r3t.linear.position[:, np.newaxis] \
               + rand_pose_3r3t.angular.dcm.dot(platform_anchor) \
               + result.lengths * result.directions == pytest.approx(
            frame_anchor)


if __name__ == "__main__":
    pytest.main()
