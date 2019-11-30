from typing import Union

# import matplotlib.pyplot as plt
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
from cdpyr.typing import (
    Num,
    Vector,
)


class GridWorkspace3R3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm in (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_cable_length(self,
                               robot_3r3t: Robot,
                               ik_standard: Kinematics,
                               archetype: Archetype,
                               lower_bound: Union[Num, Vector],
                               upper_bound: Union[Num, Vector],
                               steps: Union[Num, Vector]):
        rob = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, np.asarray(
                [0.50, 1.50]) * np.sqrt(3))

        # create the grid calculator object
        calculator = workspace.GridCalculator(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm in (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_singularities(self,
                                robot_3r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                lower_bound: Union[Num, Vector],
                                upper_bound: Union[Num, Vector],
                                steps: Union[Num, Vector]):
        rob = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the grid calculator object
        calculator = workspace.GridCalculator(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm in (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_singularities(self,
                                robot_3r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                lower_bound: Union[Num, Vector],
                                upper_bound: Union[Num, Vector],
                                steps: Union[Num, Vector]):
        rob = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the grid calculator object
        calculator = workspace.GridCalculator(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm in (np.eye(3), Angular.random().dcm)
            )
    )
    def test_3r3t_wrench_feasible(self,
                                  robot_3r3t: Robot,
                                  ik_standard: Kinematics,
                                  archetype: Archetype,
                                  lower_bound: Union[Num, Vector],
                                  upper_bound: Union[Num, Vector],
                                  steps: Union[Num, Vector]):
        rob = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 1, 10))

        # create the grid calculator object
        calculator = workspace.GridCalculator(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(rob)

    @pytest.mark.parametrize(
            ['archetype', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            [-8.0, -5.0, -0.5],
                            [8.0, 5.0, 3.0],
                            9,
                    ) for dcm in (np.eye(3), Angular.random().dcm)
            )
    )
    def test_ipanema3_wrench_feasible(self,
                                      ipanema_3: Robot,
                                      ik_standard: Kinematics,
                                      archetype: Archetype,
                                      lower_bound: Union[Num, Vector],
                                      upper_bound: Union[Num, Vector],
                                      steps: Union[Num, Vector]):
        rob = ipanema_3
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 100, 3000))

        # create the grid calculator object
        calculator = workspace.GridCalculator(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(rob)


if __name__ == "__main__":
    pytest.main()
