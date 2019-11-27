# import sys
from typing import Union

# import matplotlib.pyplot as plt
import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace
)
from cdpyr.analysis.kinematics.algorithm import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.kinematics.transformation import Angular
from cdpyr.robot import Robot
from cdpyr.typing import (
    Num,
    Vector
)


# from mpl_toolkits.mplot3d import Axes3D


class HullWorkspace3R3TTestSuite(object):

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.rotation_z(np.random.random()).dcm)
        )
    )
    def test_3r3t_cable_length(self,
                             robot_3r3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, [0.5, 1.5])

        # create the hull calculator object
        calculator = workspace.HullCalculator(ik_standard,
                                              archetype,
                                              criterion)

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.rotation_z(np.random.random()).dcm)
        )
    )
    def test_3r3t_singularities(self,
                              robot_3r3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(ik_standard,
                                              archetype,
                                              criterion)

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.rotation_z(np.random.random()).dcm)
        )
    )
    def test_3r3t_singularities(self,
                              robot_3r3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(ik_standard,
                                              archetype,
                                              criterion)

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.rotation_z(np.random.random()).dcm)
        )
    )
    def test_3r3t_wrench_feasible(self,
                               robot_3r3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
            force_distribution.ClosedFormImproved(ik_standard, 1, 10), -1)

        # create the hull calculator object
        calculator = workspace.HullCalculator(ik_standard,
                                              archetype,
                                              criterion)

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)


if __name__ == "__main__":
    pytest.main()
