import pytest
from matplotlib import use

use('MacOSX')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

import cdpyr


def plot_workspace(dims, coordinates):
    return

    # filter for the inside and outside coordinates
    inside = np.asarray(
        [coordinate[0] for coordinate in coordinates if coordinate[1]])
    outside = np.asarray(
        [coordinate[0] for coordinate in coordinates if not coordinate[1]])

    fig: plt.Figure = plt.figure()
    # three dimensional case?
    if dims == 3:
        ax: Axes3D = fig.add_subplot(111, projection='3d')
        if inside.size:
            ax.plot(inside[:, 0], inside[:, 1], inside[:, 2],
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if outside.size:
            ax.plot(outside[:, 0], outside[:, 1], outside[:, 2],
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])
    # two-dimensional case
    elif dims == 2:
        ax: plt.Axes = fig.add_subplot(111)
        if inside.size:
            ax.plot(inside[:, 0], inside[:, 1],
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if outside.size:
            ax.plot(outside[:, 0], outside[:, 1],
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])
    # one-dimensional case
    else:
        ax: plt.Axes = fig.add_subplot(111)
        if inside.size:
            ax.plot(inside[:, 0], np.zeros_like(inside[:, 0]),
                    marker='o', linestyle='None', color=[0.0, 1.0, 0.0])
        if outside.size:
            ax.plot(outside[:, 0], np.zeros_like(outside[:, 0]),
                    marker='o', markersize=2,
                    linestyle='None', color=[1.0, 0.0, 0.0])

    fig.show()


class GridWorkspaceTestSuite(object):

    def test_1t_ik_standard_translation_cable_length(self,
                                                     robot_1t:
                                                     'cdpyr.robot.Robot',
                                                     ik_standard:
                                                     'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criteria and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.CABLE_LENGTH
        criterion.limits = [0.5, 1.5]

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate of '-1.0' to
        # a maximum coordinate of '1.0'
        method.min = -1.0
        method.max = 1.0
        # along the grid, we want 51 steps which equals to 52 coordinates in
        # total including the corners
        method.step = 49

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_1t)

        plot_workspace(1, workspace)

        assert False

    def test_1t_ik_standard_translation_singularities(self,
                                                      robot_1t:
                                                      'cdpyr.robot.Robot',
                                                      ik_standard:
                                                      'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criteria and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.SINGULARITIES

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate of '-1.0' to
        # a maximum coordinate of '1.0'
        method.min = -1.0
        method.max = 1.0
        # along the grid, we want 51 steps which equals to 52 coordinates in
        # total including the corners
        method.step = 49

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_1t)

        plot_workspace(1, workspace)

        assert False

    def test_1t_ik_standard_translation_wrench_closure(self,
                                                       robot_1t:
                                                       'cdpyr.robot.Robot',
                                                       ik_standard:
                                                       'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.WRENCH_CLOSURE
        criterion.wrench = -1

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate of '-1.0' to
        # a maximum coordinate of '1.0'
        method.min = -1.0
        method.max = 1.0
        # along the grid, we want 51 steps which equals to 52 coordinates in
        # total including the corners
        method.step = 49

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_1t)

        plot_workspace(1, workspace)

        assert False

    def test_1t_ik_standard_translation_wrench_feasible(self,
                                                        robot_1t:
                                                        'cdpyr.robot.Robot',
                                                        ik_standard:
                                                        'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.WRENCH_FEASIBLE
        criterion.wrench = -1
        criterion.force_min = 1
        criterion.force_max = 10

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate of '-1.0' to
        # a maximum coordinate of '1.0'
        method.min = -1.0
        method.max = 1.0
        # along the grid, we want 51 steps which equals to 52 coordinates in
        # total including the corners
        method.step = 49

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_1t)

        plot_workspace(1, workspace)

        assert False

    def test_3r3t_ik_standard_translation_cable_length(self,
                                                       robot_3r3t:
                                                       'cdpyr.robot.Robot',
                                                       ik_standard:
                                                       'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.CABLE_LENGTH
        criterion.limits = [0.866025404, 2.598076211]

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate in the bottom
        # left rear edge of the unit cube to a maximum coordinate in the
        # right front corner of the unit cube
        method.min = [-1.0, -1.0, -1.0]
        method.max = [1.0, 1.0, 1.0]
        # along the grid, we want different steps: 4 along `x`, 4 along `y`,
        # and 9 along `z`
        method.step = [4, 4, 9]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_3r3t)

        plot_workspace(3, workspace)

        assert False

    def test_3r3t_ik_standard_translation_wrench_closure(self,
                                                         robot_3r3t:
                                                         'cdpyr.robot.Robot',
                                                         ik_standard:
                                                         'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.WRENCH_CLOSURE
        criterion.wrench = [0.0, 0.0, -9.81, 0.0, 0.0, 0.0]

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate in the bottom
        # left rear edge of the unit cube to a maximum coordinate in the
        # right front corner of the unit cube
        method.min = [-1.0, -1.0, -1.0]
        method.max = [1.0, 1.0, 1.0]
        # along the grid, we want different steps: 4 along `x`, 4 along `y`,
        # and 9 along `z`
        method.step = [4, 4, 9]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_3r3t)

        plot_workspace(3, workspace)

        assert False

    def test_3r3t_ik_standard_translation_wrench_feasible(self,
                                                          robot_3r3t:
                                                          'cdpyr.robot.Robot',
                                                          ik_standard:
                                                          'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.WRENCH_FEASIBLE
        criterion.wrench = [0.0, 0.0, -9.81, 0.0, 0.0, 0.0]
        criterion.force_min = 1
        criterion.force_max = 10

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate in the bottom
        # left rear edge of the unit cube to a maximum coordinate in the
        # right front corner of the unit cube
        method.min = [-1.0, -1.0, -1.0]
        method.max = [1.0, 1.0, 1.0]
        # along the grid, we want different steps: 4 along `x`, 4 along `y`,
        # and 9 along `z`
        method.step = [4, 4, 9]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_3r3t)

        plot_workspace(3, workspace)

        assert False

    def test_3r3t_ik_standard_translation_singularities(self,
                                                        robot_3r3t:
                                                        'cdpyr.robot.Robot',
                                                        ik_standard:
                                                        'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criterion and their parameters we want to evaluate
        criterion = cdpyr.analysis.workspace.Criterion.SINGULARITIES

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.GRID
        # configure our grid to range from a minimum coordinate in the bottom
        # left rear edge of the unit cube to a maximum coordinate in the
        # right front corner of the unit cube
        method.min = [-1.0, -1.0, -1.0]
        method.max = [1.0, 1.0, 1.0]
        # along the grid, we want different steps: 4 along `x`, 4 along `y`,
        # and 9 along `z`
        method.step = [4, 4, 9]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criterion,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace = workspace_calculator.evaluate(robot_3r3t)

        plot_workspace(3, workspace)

        assert False


if __name__ == "__main__":
    pytest.main()
