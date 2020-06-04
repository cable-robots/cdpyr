from __future__ import annotations

import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.criterion import Singularities, CableLength, WrenchFeasible
from cdpyr.analysis.kinematics.kinematics import Algorithm as Kinematics
from cdpyr.analysis import archetype
from cdpyr.analysis.archetype.archetype import Archetype
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class HullWorkspace3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype', 'parallel'],
            (
                    (
                            archetype.Translation(np.eye(3)),
                            parallel,
                    ) for parallel in (False, True)
            )
    )
    def test_3t_cable_length(self,
                             robot_3t: Robot,
                             ik_standard: Kinematics,
                             archetype: Archetype,
                             parallel: bool):
        robot = robot_3t
        # create the criterion
        criterion = CableLength(ik_standard, np.asarray(
                [0.5, 1.5]) * np.sqrt(3))

        # create the hull calculator object
        calculator = workspace.hull.Algorithm(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)

    @pytest.mark.parametrize(
            ['archetype', 'parallel'],
            (
                    (
                            archetype.Translation(np.eye(3)),
                            parallel,
                    ) for parallel in (False, True)
            )
    )
    def test_3t_singularities(self,
                              robot_3t: Robot,
                              ik_standard: Kinematics,
                              archetype: Archetype,
                              parallel: bool):
        robot = robot_3t
        # create the criterion
        criterion = Singularities(ik_standard)

        # create the hull calculator object
        calculator = workspace.hull.Algorithm(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)

    @pytest.mark.parametrize(
            ['archetype', 'parallel'],
            (
                    (
                            archetype.Translation(np.eye(3)),
                            parallel,
                    ) for parallel in (False, True)
            )
    )
    def test_3t_wrench_feasible(self,
                                robot_3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                parallel: bool):
        robot = robot_3t
        # create the criterion
        criterion = WrenchFeasible(
                force_distribution.ClosedFormImproved(ik_standard, 1, 10))

        # create the hull calculator object
        calculator = workspace.hull.Algorithm(archetype,
                                              criterion,
                                              center=[0.0, 0.0, 0.0])

        # evaluate workspace
        workspace_hull = calculator.evaluate(robot, parallel=parallel,
                                             verbose=20)


if __name__ == "__main__":
    pytest.main()
