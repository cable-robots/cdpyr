import numpy as np
import pytest

import cdpyr


class ClosedFormImprovedorceDistributionTestSuite(object):

    def test_1t(self,
                robot_1t: cdpyr.robot.Robot,
                empty_pose: cdpyr.motion.Pose,
                ik_standard: cdpyr.analysis.kinematics.algorithm.Algorithm):
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_1t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[0] = -9.81 * 0.1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_1t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_1t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()

    def test_2t(self,
                robot_2t: cdpyr.robot.Robot,
                empty_pose: cdpyr.motion.Pose,
                ik_standard):
        # force distribution solver
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_2t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_2t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_2t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()

    def test_3t(self,
                robot_3t: cdpyr.robot.Robot,
                empty_pose: cdpyr.motion.Pose,
                ik_standard):
        # force distribution solver
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_3t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_3t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()

    def test_1r2t(self,
                  robot_1r2t: cdpyr.robot.Robot,
                  empty_pose: cdpyr.motion.Pose,
                  ik_standard):
        # force distribution solver
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_1r2t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_1r2t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_1r2t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()

    def test_2r3t(self,
                  robot_2r3t: cdpyr.robot.Robot,
                  empty_pose: cdpyr.motion.Pose,
                  ik_standard):
        # force distribution solver
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_2r3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_2r3t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_2r3t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()

    def test_3r3t(self,
                  robot_3r3t: cdpyr.robot.Robot,
                  empty_pose: cdpyr.motion.Pose,
                  ik_standard):
        # force distribution solver
        closed_form_improved = \
            cdpyr.analysis.force_distribution.ClosedFormImproved(
                ik_standard,
                force_minimum=1,
                force_maximum=10
            )

        # create a gravitational wrench
        wrench = np.zeros(robot_3r3t.platforms[0].dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        distribution = closed_form_improved.evaluate(
            robot_3r3t,
            empty_pose,
            wrench,
        )

        # assertion
        assert distribution.pose == empty_pose
        assert distribution.distribution.ndim == 1
        assert distribution.distribution.shape == (
            robot_3r3t.num_kinematic_chains,)
        assert (distribution.distribution > 0).all()


if __name__ == "__main__":
    pytest.main()
