import numpy as np
import pytest

from cdpyr import (
    analysis,
    visualization
)
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class plotlyPlotHullWorkspaceTestSuite(object):

    def test_plot_hull_3t(self,
                           tmpdir,
                           robot_3t: Robot,
                           ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.HullCalculator(archetype,
                                                       criterion,
                                                       center=[0.0, 0.0, 0.0])
        workspace = calculator.evaluate(robot_3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_hull_2r3t(self,
                             tmpdir,
                             robot_2r3t: Robot,
                             ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.HullCalculator(archetype,
                                                       criterion,
                                                       center=[0.0, 0.0, 0.0])
        workspace = calculator.evaluate(robot_2r3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_2r3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()

    def test_plot_hull_3r3t(self,
                                 tmpdir,
                                 robot_3r3t: Robot,
                                 ik_standard: analysis.kinematics.Standard):
        # calculate the cable length workspace (because that's never gonna fail)
        criterion = analysis.workspace.criterion.CableLength(
            ik_standard, np.asarray([0.50, 1.50]) * np.sqrt(3))
        archetype = analysis.workspace.archetype.Translation(np.eye(3))
        calculator = analysis.workspace.HullCalculator(archetype,
                                                       criterion,
                                                       center=[0.0, 0.0, 0.0])
        workspace = calculator.evaluate(robot_3r3t)

        # visualize result
        visualizer = visualization.plotly.Spatial()
        visualizer.render(robot_3r3t)
        visualizer.render(workspace)
        visualizer.draw()
        visualizer.show()


if __name__ == "__main__":
    pytest.main()
