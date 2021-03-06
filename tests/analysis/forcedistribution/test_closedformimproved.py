import numpy as np
import pytest

from cdpyr.analysis.force_distribution import closed_form_improved
from cdpyr.analysis.kinematics.standard import Standard as StandardKinematics
from cdpyr.motion.pose import Pose
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ClosedFormImprovedorceDistributionTestSuite(object):

    def test_1t(self,
                robot_1t: Robot,
                zero_pose: Pose,
                ik_standard: StandardKinematics):
        solver = closed_form_improved.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
        )

        # create a gravitational wrench
        wrench = np.zeros(robot_1t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[0] = -9.81 * 0.1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_1t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_1t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()

    def test_2t(self,
                robot_2t: Robot,
                zero_pose: Pose,
                ik_standard: StandardKinematics):
        # force distribution solver
        solver = \
            closed_form_improved.ClosedFormImproved(
                    ik_standard,
                    force_minimum=1,
                    force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_2t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_2t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_2t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()

    def test_3t(self,
                robot_3t: Robot,
                zero_pose: Pose,
                ik_standard: StandardKinematics):
        # force distribution solver
        solver = \
            closed_form_improved.ClosedFormImproved(
                    ik_standard,
                    force_minimum=1,
                    force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_3t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_3t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()

    def test_1r2t(self,
                  robot_1r2t: Robot,
                  zero_pose: Pose,
                  ik_standard: StandardKinematics):
        # force distribution solver
        solver = \
            closed_form_improved.ClosedFormImproved(
                    ik_standard,
                    force_minimum=1,
                    force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_1r2t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_1r2t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_1r2t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()

    def test_2r3t(self,
                  robot_2r3t: Robot,
                  zero_pose: Pose,
                  ik_standard: StandardKinematics):
        # force distribution solver
        solver = \
            closed_form_improved.ClosedFormImproved(
                    ik_standard,
                    force_minimum=1,
                    force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_2r3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_2r3t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_2r3t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()

    def test_3r3t(self,
                  robot_3r3t: Robot,
                  zero_pose: Pose,
                  ik_standard: StandardKinematics):
        # force distribution solver
        solver = \
            closed_form_improved.ClosedFormImproved(
                    ik_standard,
                    force_minimum=1,
                    force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_3r3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = solver.evaluate(
                robot_3r3t,
                zero_pose,
                wrench,
        )

        # assertion
        assert distribution.pose == zero_pose
        assert distribution.forces.ndim == 1
        assert distribution.forces.shape == (
            robot_3r3t.num_kinematic_chains,)
        assert (distribution.forces > 0).all()


if __name__ == "__main__":
    pytest.main()
