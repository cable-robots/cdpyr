import pytest

from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.analysis.structure_matrix.calculator import Calculator as StructureMatrixCalculator
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot


class StructureMatrixTestSuite(object):

    def test_1t(self,
                robot_1t: Robot,
                rand_pose_1t: Pose,
                ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_1t, rand_pose_1t)

        assert structmat.pose == rand_pose_1t
        assert structmat.matrix.shape == (1, robot_1t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace

    def test_2t(self,
                robot_2t: Robot,
                rand_pose_2t: Pose,
                ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_2t, rand_pose_2t)

        assert structmat.pose == rand_pose_2t
        assert structmat.matrix.shape == (2, robot_2t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace

    def test_3t(self,
                robot_3t: Robot,
                rand_pose_3t: Pose,
                ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_3t, rand_pose_3t)

        assert structmat.pose == rand_pose_3t
        assert structmat.matrix.shape == (3, robot_3t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace

    def test_1r2t(self,
                  robot_1r2t: Robot,
                  rand_pose_1r2t: Pose,
                  ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_1r2t, rand_pose_1r2t)

        assert structmat.pose == rand_pose_1r2t
        assert structmat.matrix.shape == (3, robot_1r2t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace

    def test_2r3t(self,
                  robot_2r3t: Robot,
                  rand_pose_2r3t: Pose,
                  ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_2r3t, rand_pose_2r3t)

        assert structmat.pose == rand_pose_2r3t
        assert structmat.matrix.shape == (5, robot_2r3t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace

    def test_3r3t(self,
                  robot_3r3t: Robot,
                  rand_pose_3r3t: Pose,
                  ik_standard: StandardKinematics):
        sms = StructureMatrixCalculator(ik_standard)
        structmat = sms.evaluate(robot_3r3t, rand_pose_3r3t)

        assert structmat.pose == rand_pose_3r3t
        assert structmat.matrix.shape == (6, robot_3r3t.num_kinematic_chains)
        assert structmat.nullspace.shape[0] == structmat.matrix.shape[1]
        assert structmat.kernel is structmat.nullspace
        assert structmat.null_space is structmat.nullspace


if __name__ == "__main__":
    pytest.main()
