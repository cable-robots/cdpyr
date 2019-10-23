import numpy as np
import pytest

import cdpyr


class ClosedFormForceDistributionTestSuite(object):

    def test_1t(self,
                robot_1t: cdpyr.robot.Robot,
                empty_pose,
                ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_1t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_1t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_1t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[0] = -9.81 * 0.1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_1t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_1t.num_cables,)
        assert (force_distribution > 0).all()

    def test_2t(self,
                robot_2t: cdpyr.robot.Robot,
                empty_pose,
                ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_2t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_2t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_2t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_2t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_2t.num_cables,)
        assert (force_distribution > 0).all()

    def test_3t(self,
                robot_3t: cdpyr.robot.Robot,
                empty_pose,
                ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_3t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_3t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_3t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_3t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_3t.num_cables,)
        assert (force_distribution > 0).all()

    def test_1r2t(self,
                  robot_1r2t: cdpyr.robot.Robot,
                  empty_pose,
                  ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_1r2t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_1r2t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_1r2t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[1] = -9.81 * 1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_1r2t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_1r2t.num_cables,)
        assert (force_distribution > 0).all()

    def test_2r3t(self,
                  robot_2r3t: cdpyr.robot.Robot,
                  empty_pose,
                  ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_2r3t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_2r3t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_2r3t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_2r3t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_2r3t.num_cables,)
        assert (force_distribution > 0).all()

    def test_3r3t(self,
                  robot_3r3t: cdpyr.robot.Robot,
                  empty_pose,
                  ik_standard):
        # solve inverse kinematics
        _, uis = ik_standard.backward(robot_3r3t, empty_pose)

        # get structure matrix for the current pose
        sms = cdpyr.analysis.structurematrix.Calculator()
        structmat = sms.evaluate(robot_3r3t, uis, empty_pose)

        # force distribution solver
        fdist = cdpyr.analysis.forcedistribution.Calculator.CLOSED_FORM

        # create a gravitational wrench
        wrench = np.zeros(robot_3r3t.platforms[0].motionpattern.dof)
        # add gravity at last translational degree of freedom
        wrench[2] = -9.81 * 1

        # and calculate force distribution
        force_distribution: cdpyr.typing.Vector = fdist.evaluate(
            robot_3r3t,
            structmat,
            wrench,
            force_min=1,
            force_max=10,
        )

        # assertion
        assert force_distribution.ndim == 1
        assert force_distribution.shape == (robot_3r3t.num_cables,)
        assert (force_distribution > 0).all()


if __name__ == "__main__":
    pytest.main()
