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


class HullWorkspace3TTestSuite(object):

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.random().dcm)
        )
    )
    def test_3t_cable_length(self,
                             robot_3t: Robot,
                             ik_standard: Kinematics,
                             archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, [0.5, 1.5])

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.random().dcm)
        )
    )
    def test_3t_singularities(self,
                              robot_3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.random().dcm)
        )
    )
    def test_3t_singularities(self,
                              robot_3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3t)

    @pytest.mark.parametrize(
        ['archetype'],
        (
            (
                [workspace.archetype.Translation(dcm)]
            ) for dcm in (np.eye(3), Angular.random().dcm)
        )
    )
    def test_3t_wrench_feasible(self,
                                robot_3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
            force_distribution.ClosedFormImproved(ik_standard, 1, 10))

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3t)


if __name__ == "__main__":
    pytest.main()
