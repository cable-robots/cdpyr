import numpy as np
import pytest

from cdpyr import (
    analysis,
    visualization
)
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotlyGridGridWorkspaceTestSuite(object):

    def test_plot_grid_1t(self,
                           tmpdir,
                           robot_1t: Robot,
                           ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.5, 1.5]))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=-1,
                                                       upper_bound=1,
                                                       steps=9)
        workspace = calculator.evaluate(robot_1t)

        # visualize result
        visualizer = visualization.plotly.Linear()
        visualizer.render(robot_1t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_grid_2t(self,
                           tmpdir,
                           robot_2t: Robot,
                           ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(2))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=[-1, -1],
                                                       upper_bound=[1, 1],
                                                       steps=9)
        workspace = calculator.evaluate(robot_2t)

        # visualize result
        visualizer = visualization.plotly.Planar()
        visualizer.render(robot_2t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_grid_3t(self,
                           tmpdir,
                           robot_3t: Robot,
                           ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=[-1, -1, -1],
                                                       upper_bound=[1, 1, 1],
                                                       steps=9)
        workspace = calculator.evaluate(robot_3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_grid_1r2t(self,
                             tmpdir,
                             robot_1r2t: Robot,
                             ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(2))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=[-1, -1],
                                                       upper_bound=[1, 1],
                                                       steps=9)
        workspace = calculator.evaluate(robot_1r2t)

        # visualize result
        visualizer = visualization.plotly.Planar()
        visualizer.render(robot_1r2t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_grid_2r3t(self,
                             tmpdir,
                             robot_2r3t: Robot,
                             ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=[-1, -1, -1],
                                                       upper_bound=[1, 1, 1],
                                                       steps=9)
        workspace = calculator.evaluate(robot_2r3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_2r3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_grid_3r3t(self,
                                 tmpdir,
                                 robot_3r3t: Robot,
                                 ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.GridCalculator(archetype,
                                                       criterion,
                                                       lower_bound=[-1, -1, -1],
                                                       upper_bound=[1, 1, 1],
                                                       steps=9)
        workspace = calculator.evaluate(robot_3r3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_3r3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()


if __name__ == "__main__":
    pytest.main()
