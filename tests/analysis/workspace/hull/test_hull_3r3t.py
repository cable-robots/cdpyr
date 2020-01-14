import itertools

import numpy as np
import pytest

from cdpyr.analysis import (
    force_distribution,
    workspace,
)
from cdpyr.analysis.kinematics.kinematics import Algorithm as Kinematics
from cdpyr.analysis.workspace.archetype.archetype import Archetype
from cdpyr.kinematics.transformation.angular import Angular
from cdpyr.robot import Robot


class HullWorkspace3R3TTestSuite(object):

    @pytest.mark.parametrize(
            ['archetype', 'parallel'],
            (
                    (
                            workspace.archetype.Translation(dcm),
                            parallel,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_3r3t_cable_length(self,
                               robot_3r3t: Robot,
                               ik_standard: Kinematics,
                               archetype: Archetype,
                               parallel: bool):
        robot = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.CableLength(ik_standard, np.asarray(
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
                            workspace.archetype.Translation(dcm),
                            parallel,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_3r3t_singularities(self,
                                robot_3r3t: Robot,
                                ik_standard: Kinematics,
                                archetype: Archetype,
                                parallel: bool):
        robot = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.Singularities(ik_standard)

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
                            workspace.archetype.Translation(dcm),
                            parallel,
                    ) for dcm, parallel in
            itertools.product((np.eye(3), Angular.random().dcm), (False, True))
            )
    )
    def test_3r3t_wrench_feasible(self,
                                  robot_3r3t: Robot,
                                  ik_standard: Kinematics,
                                  archetype: Archetype,
                                  parallel: bool):
        robot = robot_3r3t
        # create the criterion
        criterion = workspace.criterion.WrenchFeasible(
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
