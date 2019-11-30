import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.kinematics.algorithm import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.robot import Robot


class HullWorkspace3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype'],
            [
                [workspace.archetype.Translation(np.eye(3))]
            ]
    )
    def test_3t_cable_length(self,
                             robot_3t: Robot,
                             ik_standard: Kinematics,
                             archetype: Archetype):
        rob = robot_3t
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, np.asarray(
                [0.5, 1.5]) * np.sqrt(3))

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype'],
            [
                [workspace.archetype.Translation(np.eye(3))]
            ]
    )
    def test_3t_singularities(self,
                              robot_3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype):
        rob = robot_3t
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype'],
            [
                [workspace.archetype.Translation(np.eye(3))]
            ]
    )
    def test_3t_wrench_feasible(self,
                                robot_3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype):
        rob = robot_3t
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 1, 10))

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(rob)


if __name__ == "__main__":
    pytest.main()
