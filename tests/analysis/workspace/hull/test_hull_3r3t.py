import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.kinematics.algorithm import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.kinematics.transformation import Angular
from cdpyr.robot import Robot


class HullWorkspace3R3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype'],
            (
                    (
                            [workspace.archetype.Translation(dcm)]
                    ) for dcm in
                    (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_cable_length(self,
                               robot_3r3t: Robot,
                               ik_standard: Kinematics,
                               archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, [0.5, 1.5])

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
            ['archetype'],
            (
                    (
                            [workspace.archetype.Translation(dcm)]
                    ) for dcm in
                    (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_singularities(self,
                                robot_3r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
            ['archetype'],
            (
                    (
                            [workspace.archetype.Translation(dcm)]
                    ) for dcm in
                    (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_singularities(self,
                                robot_3r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_result = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
            ['archetype'],
            (
                    (
                            [workspace.archetype.Translation(dcm)]
                    ) for dcm in
                    (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_wrench_feasible(self,
                                  robot_3r3t: Robot,
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
        hull_workspace = calculator.evaluate(robot_3r3t)

    @pytest.mark.parametrize(
            ['archetype'],
            (
                    (
                            [workspace.archetype.Translation(dcm)]
                    ) for dcm in
                    (np.eye(3), Angular.random().dcm)
            )
    )
    def test_ipanema_3_wrench_feasible(self,
                                       ipanema_3: Robot,
                                       ik_standard: Kinematics,
                                       archetype: Archetype):
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 120, 3000))

        # create the hull calculator object
        calculator = workspace.HullCalculator(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0],
                                              maximum_iterations=25,
                                              depth=4 )

        # evaluate workspace
        hull_workspace = calculator.evaluate(ipanema_3)


if __name__ == "__main__":
    pytest.main()
