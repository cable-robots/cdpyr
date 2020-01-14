import itertools
from typing import Union

import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.kinematics.kinematics import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.kinematics.transformation import Angular
from cdpyr.robot import Robot
from cdpyr.typing import (
    Num,
    Vector,
)


class GridWorkspace2R3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype', 'parallel', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            parallel,
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_2r3t_cable_length(self,
                               robot_2r3t: Robot,
                               ik_standard: Kinematics,
                               archetype: Archetype,
                               parallel: bool,
                               lower_bound: Union[Num, Vector],
                               upper_bound: Union[Num, Vector],
                               steps: Union[Num, Vector]):
        robot = robot_2r3t
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, np.asarray(
                [0.50, 1.50]) * np.sqrt(3))

        # create the grid calculator object
        calculator = workspace.grid.Algorithm(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)

    @pytest.mark.parametrize(
            ['archetype', 'parallel', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            parallel,
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_2r3t_singularities(self,
                                robot_2r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                parallel: bool,
                                lower_bound: Union[Num, Vector],
                                upper_bound: Union[Num, Vector],
                                steps: Union[Num, Vector]):
        robot = robot_2r3t
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

        # create the grid calculator object
        calculator = workspace.grid.Algorithm(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)

    @pytest.mark.parametrize(
            ['archetype', 'parallel', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            parallel,
                            [-1.0, -1.0, -1.0],
                            [1.0, 1.0, 1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_2r3t_wrench_feasible(self,
                                  robot_2r3t: Robot,
                                  ik_standard: Kinematics,
                                  archetype: Archetype,
                                  parallel: bool,
                                  lower_bound: Union[Num, Vector],
                                  upper_bound: Union[Num, Vector],
                                  steps: Union[Num, Vector]):
        robot = robot_2r3t
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 1, 10))

        # create the grid calculator object
        calculator = workspace.grid.Algorithm(archetype,
                                              criterion,
                                              lower_bound,
                                              upper_bound,
                                              steps)

        # evaluate workspace
        workspace_grid = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)


if __name__ == "__main__":
    pytest.main()
