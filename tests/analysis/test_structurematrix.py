from __future__ import annotations

import numpy as np
import pytest

from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.analysis.structure_matrix.calculator import Calculator as \
    StructureMatrixCalculator
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class StructureMatrixTestSuite(object):

    def test_1t(self,
                robot_1t: Robot,
                rand_pose_1t: Pose,
                ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_1t
        pose = rand_pose_1t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_1t, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:1, :], axis=0), 1)

    def test_2t(self,
                robot_2t: Robot,
                rand_pose_2t: Pose,
                ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_2t
        pose = rand_pose_2t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:2, :], axis=0), 1)

    def test_3t(self,
                robot_3t: Robot,
                rand_pose_3t: Pose,
                ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_3t
        pose = rand_pose_3t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:3, :], axis=0), 1)

    def test_1r2t(self,
                  robot_1r2t: Robot,
                  rand_pose_1r2t: Pose,
                  ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_1r2t
        pose = rand_pose_1r2t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:2, :], axis=0), 1)

    def test_2r3t(self,
                  robot_2r3t: Robot,
                  rand_pose_2r3t: Pose,
                  ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_2r3t
        pose = rand_pose_2r3t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:3, :], axis=0), 1)

    def test_3r3t(self,
                  robot_3r3t: Robot,
                  rand_pose_3r3t: Pose,
                  ik_standard: StandardKinematics):
        # shift arguments for consistency
        robot = robot_3r3t
        pose = rand_pose_3r3t

        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot, pose)

        assert structmat.pose == pose
        assert structmat.matrix.shape == (robot.num_dof, robot.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace
        # check ui's are all of unit length
        assert np.allclose(np.linalg.norm(structmat.matrix[0:3, :], axis=0), 1)


if __name__ == "__main__":
    pytest.main()
