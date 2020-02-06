import itertools
from typing import Union

import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.criterion import CableLength, Singularities, WrenchFeasible
from cdpyr.analysis.kinematics.kinematics import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.robot import Robot
from cdpyr.typing import (
    Num,
    Vector,
)


class GridWorkspace1TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype', 'parallel', 'lower_bound', 'upper_bound', 'steps'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            parallel,
                            [-1.0],
                            [1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3),), (False, True))
            )
    )
    def test_1t_cable_length(self,
                             robot_1t: Robot,
                             ik_standard: Kinematics,
                             archetype: Archetype,
                             parallel: bool,
                             lower_bound: Union[Num, Vector],
                             upper_bound: Union[Num, Vector],
                             steps: Union[Num, Vector]):
        robot = robot_1t
        # create the criterion
        criterion = CableLength(ik_standard, np.asarray(
                [0.50, 1.50]) * np.sqrt(2))

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
                            [-1.0],
                            [1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3),), (False, True))
            )
    )
    def test_1t_singularities(self,
                              robot_1t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype,
                              parallel: bool,
                              lower_bound: Union[Num, Vector],
                              upper_bound: Union[Num, Vector],
                              steps: Union[Num, Vector]):
        robot = robot_1t
        # create the criterion
        criterion = Singularities(ik_standard)

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
                            [-1.0],
                            [1.0],
                            9,
                    ) for dcm, parallel in
            itertools.product((np.eye(3),), (False, True))
            )
    )
    def test_1t_wrench_feasible(self,
                                robot_1t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                parallel: bool,
                                lower_bound: Union[Num, Vector],
                                upper_bound: Union[Num, Vector],
                                steps: Union[Num, Vector]):
        robot = robot_1t
        # create the criterion
        criterion = WrenchFeasible(
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
