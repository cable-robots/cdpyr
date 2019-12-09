import numpy as np
import pytest

from cdpyr.analysis.kinematics.pulley import Pulley as PulleyKinematics
from cdpyr.kinematics.transformation import Angular
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot


class PulleyKinematicsBackwardTestSuite(object):

    def test_motion_pattern_1t(self,
                               robot_1t: Robot,
                               rand_pose_1t: Pose,
                               ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_1t
        robot = robot_1t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (1, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]

            # go to cable leave point via platform
            a = platform_position[0:1] + sol.directions[:,chain_index] * (sol.joints[chain_index] - pulley.radius *sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b[0:1])
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position)

    def test_motion_pattern_2t(self,
                               robot_2t: Robot,
                               rand_pose_2t: Pose,
                               ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_2t
        robot = robot_2t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (2, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]

            # go to cable leave point via platform
            a = platform_position[0:2] + sol.directions[:,chain_index] * (sol.joints[chain_index] - pulley.radius *sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b[0:2])
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position)

    def test_motion_pattern_3t(self,
                               robot_3t: Robot,
                               rand_pose_3t: Pose,
                               ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_3t
        robot = robot_3t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (3, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]

            # go to cable leave point via platform
            a = platform_position + platform_dcm.dot(
                    platform_anchor.linear.position) + sol.directions[:,
                                                       chain_index] * (
                        sol.joints[chain_index] - pulley.radius *
                        sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b)
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position)

    def test_motion_pattern_1r2t(self,
                                 robot_1r2t: Robot,
                                 rand_pose_1r2t: Pose,
                                 ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_1r2t
        robot = robot_1r2t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (2, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]

            # go to cable leave point via platform
            a = platform_position[0:2] + platform_dcm[0:2,0:2].dot(
                    platform_anchor.linear.position[0:2]) + sol.directions[:,
                                                       chain_index] * (
                        sol.joints[chain_index] - pulley.radius *
                        sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b[0:2])
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position + platform_dcm.dot(
                    platform_anchor.linear.position))

    def test_motion_pattern_2r3t(self,
                                 robot_2r3t: Robot,
                                 rand_pose_2r3t: Pose,
                                 ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_2r3t
        robot = robot_2r3t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (3, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]

            # go to cable leave point via platform
            a = platform_position + platform_dcm.dot(
                    platform_anchor.linear.position) + sol.directions[:,
                                                       chain_index] * (
                        sol.joints[chain_index] - pulley.radius *
                        sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b)
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position + platform_dcm.dot(
                    platform_anchor.linear.position))

    def test_motion_pattern_3r3t(self,
                                 robot_3r3t: Robot,
                                 rand_pose_3r3t: Pose,
                                 ik_pulley: PulleyKinematics):
        # shift so we can copy code more easily from one test case to another
        pose = rand_pose_3r3t
        robot = robot_3r3t

        # solve the kinematics
        sol = ik_pulley.backward(robot, pose)

        # get platform position and orientation
        platform_position, platform_dcm = pose.position

        # directions should match spatial domain and the number of kinematic
        # chains
        assert sol.directions.shape == (3, robot.num_kinematic_chains)
        # cable lengths should be non-zero
        assert not np.allclose(sol.lengths, 0)
        # all swivel angles should be non-zero
        assert not np.allclose(sol.swivel_angles, 0)
        # all wrap angles should be non-zeros
        assert not np.allclose(sol.wrap_angles, 0)
        # get the cable shape
        cable_shapes = sol.cable_shapes
        assert not np.allclose(cable_shapes, 0)

        # loop over each kinematic chain and close the loop ensuring that
        # getting to the cable leave via the frame anchor is the same as via the
        # platform
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            pulley = frame_anchor.pulley
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]

            # go to cable leave point via platform
            a = platform_position + platform_dcm.dot(
                    platform_anchor.linear.position) + sol.directions[:,
                                                       chain_index] * (
                        sol.joints[chain_index] - pulley.radius *
                        sol.wrap_angles[chain_index])
            cable_dcm = Angular.rotation_z(sol.swivel_angles[chain_index]).dcm
            wrap_dcm = Angular.rotation_y(sol.wrap_angles[chain_index]).dcm
            b = frame_anchor.linear.position + frame_anchor.dcm.dot(
                    pulley.dcm.dot(cable_dcm.dot(
                            [pulley.radius, 0, 0] + wrap_dcm.dot(
                                    [-pulley.radius, 0, 0]))))
            assert np.allclose(a, b)
            assert np.allclose(cable_shapes[:,chain_index,0], frame_anchor.linear.position)
            assert np.allclose(cable_shapes[:,chain_index,-1], platform_position + platform_dcm.dot(
                    platform_anchor.linear.position))


if __name__ == "__main__":
    pytest.main()
