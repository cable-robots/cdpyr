import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest
from mpl_toolkits.mplot3d import Axes3D

from cdpyr.analysis import force_distribution, workspace
from cdpyr.analysis.kinematics.algorithm import Algorithm as Kinematics
from cdpyr.robot import Robot


def plot_workspace(dims, ws: workspace.GRID_RESULT, title):
    return

    fig: plt.Figure = plt.figure()
    # three dimensional case?
    if dims == 3:
        ax: Axes3D = fig.add_subplot(111, projection='3d')
        if ws.inside.size:
            ax.plot(ws.inside[:, 0], ws.inside[:, 1], ws.inside[:, 2],
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if ws.outside.size:
            ax.plot(ws.outside[:, 0], ws.outside[:, 1], ws.outside[:, 2],
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])
    # two-dimensional case
    elif dims == 2:
        ax: plt.Axes = fig.add_subplot(111)
        if ws.inside.size:
            ax.plot(ws.inside[:, 0], ws.inside[:, 1],
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if ws.outside.size:
            ax.plot(ws.outside[:, 0], ws.outside[:, 1],
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])
    # one-dimensional case
    else:
        ax: plt.Axes = fig.add_subplot(111)
        if ws.inside.size:
            ax.plot(ws.inside[:, 0], np.zeros_like(ws.inside[:, 0]),
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if ws.outside.size:
            ax.plot(ws.outside[:, 0], np.zeros_like(ws.outside[:, 0]),
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])

    # add a title so figures can be more easily distinguished
    plt.title(title)

    fig.show()


class GridWorkspaceTestSuite(object):

    def test_1t_ik_standard_translation_cable_length(self,
                                                     robot_1t: Robot,
                                                     ik_standard: Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and its parameters we want to evaluate
        criterion = workspace.criterion.CABLE_LENGTH(
            kinematics=ik_standard,
            limits=[0.5, 1.5]
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0' to
            # a maximum coordinate of '1.0'
            lower_bound=-1.0,
            upper_bound=1.0,
            # along the grid, we want 51 steps which equals to 52 coordinates in
            # total including the corners
            step=49
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_1t)

        plot_workspace(1, ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert 0.0 in ws
        assert 0.4 in ws
        assert 0.6 not in ws
        assert 1.0 not in ws

    def test_1t_ik_standard_translation_singularities(self,
                                                      robot_1t: Robot,
                                                      ik_standard: Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criteria and their parameters we want to evaluate
        criterion = workspace.criterion.SINGULARITIES(
            kinematics=ik_standard
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0' to
            # a maximum coordinate of '1.0'
            lower_bound=-1.0,
            upper_bound=1.0,
            # along the grid, we want 51 steps which equals to 52 coordinates in
            # total including the corners
            step=49
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_1t)

        plot_workspace(1, ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert 0.0 in ws
        assert 0.4 in ws
        assert 0.6 in ws
        assert 1.0 in ws

    def test_1t_ik_standard_translation_wrench_closure(self,
                                                       robot_1t: Robot,
                                                       ik_standard: Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_CLOSURE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[1],
                force_maximum=[10],
            ),
            wrench=-1
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0' to
            # a maximum coordinate of '1.0'
            lower_bound=-1.0,
            upper_bound=1.0,
            # along the grid, we want 51 steps which equals to 52 coordinates in
            # total including the corners
            step=49
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_1t)

        plot_workspace(1, ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert 0.0 in ws
        assert 0.4 in ws
        assert 0.6 in ws
        assert 1.0 in ws

    def test_1t_ik_standard_translation_wrench_feasible(self,
                                                        robot_1t: Robot,
                                                        ik_standard:
                                                        Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_FEASIBLE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[0],
                force_maximum=[np.inf]
            ),
            wrench=-1
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0' to
            # a maximum coordinate of '1.0'
            lower_bound=-1.0,
            upper_bound=1.0,
            # along the grid, we want 51 steps which equals to 52 coordinates in
            # total including the corners
            step=49
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_1t)

        plot_workspace(1, ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert 0.0 in ws
        assert 0.4 in ws
        assert 0.6 in ws
        assert 1.0 in ws

    def test_3r3t_ik_standard_translation_cable_length(self,
                                                       robot_3r3t: Robot,
                                                       ik_standard:
                                                       Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and its parameters we want to evaluate
        criterion = workspace.criterion.CABLE_LENGTH(
            kinematics=ik_standard,
            limits=[0.866025404, 2.598076211]
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0'
            # to a maximum coordinate of '1.0'
            lower_bound=[-1.0, -1.0, -1.0],
            upper_bound=[1.0, 1.0, 1.0],
            # along the grid, we want 51 steps which equals to 52 coordinates
            # in total including the corners
            step=[4, 4, 9]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(3, ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.4, 0.4, 0.4] not in ws
        assert [0.6, 0.6, 0.6] not in ws
        assert [1.0, 1.0, 1.0] not in ws

    def test_3r3t_ik_standard_translation_wrench_closure(self,
                                                         robot_3r3t: Robot,
                                                         ik_standard:
                                                         Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_CLOSURE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[1],
                force_maximum=[10]
            ),
            wrench=[0.0, 0.0, -9.81, 0.0, 0.0, 0.0]
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0'
            # to a maximum coordinate of '1.0'
            lower_bound=[-1.0, -1.0, -1.0],
            upper_bound=[1.0, 1.0, 1.0],
            # along the grid, we want 51 steps which equals to 52 coordinates
            # in total including the corners
            step=[4, 4, 9]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(3, ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.4, 0.4, 0.4] in ws
        assert [0.6, 0.6, 0.6] in ws
        assert [1.0, 1.0, 1.0] in ws

    def test_3r3t_ik_standard_translation_wrench_feasible(self,
                                                          robot_3r3t: Robot,
                                                          ik_standard:
                                                          Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_FEASIBLE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[0],
                force_maximum=[np.inf]
            ),
            wrench=[0.0, 0.0, -9.81, 0.0, 0.0, 0.0]
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0'
            # to a maximum coordinate of '1.0'
            lower_bound=[-1.0, -1.0, -1.0],
            upper_bound=[1.0, 1.0, 1.0],
            # along the grid, we want 51 steps which equals to 52 coordinates
            # in total including the corners
            step=[4, 4, 9]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(3, ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.4, 0.4, 0.4] in ws
        assert [0.6, 0.6, 0.6] in ws
        assert [1.0, 1.0, 1.0] in ws

    def test_3r3t_ik_standard_translation_singularities(self,
                                                        robot_3r3t: Robot,
                                                        ik_standard:
                                                        Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criteria and their parameters we want to evaluate
        criterion = workspace.criterion.SINGULARITIES(
            kinematics=ik_standard
        )

        # method we want to use to calculate the workspace
        method = workspace.GRID(
            ik_standard,
            archetype,
            criterion,
            # configure our grid to range from a minimum coordinate of '-1.0'
            # to a maximum coordinate of '1.0'
            lower_bound=[-1.0, -1.0, -1.0],
            upper_bound=[1.0, 1.0, 1.0],
            # along the grid, we want 51 steps which equals to 52 coordinates
            # in total including the corners
            step=[4, 4, 9]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(3, ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert [0.0, 0.0, 0.0] not in ws
        assert [0.4, 0.4, 0.4] not in ws
        assert [0.6, 0.6, 0.6] not in ws
        assert [1.0, 1.0, 1.0] not in ws


if __name__ == "__main__":
    pytest.main()
