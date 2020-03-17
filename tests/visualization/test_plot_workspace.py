import itertools

import numpy as np
import pytest

from cdpyr import (
    visualization
)
from cdpyr.analysis import workspace, archetype, criterion
from cdpyr.analysis.kinematics import Standard
from cdpyr.robot import sample as robots
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotWorkspaceTestSuite(object):

    @pytest.mark.parametrize(
        ('wizard', 'robot', 'ws_algorithm'),
        (
            (visualization.Visualizer(
                visualization.engine.plotly.Linear()),
             rob,
             workspace.grid.Algorithm(
                 archetype.Translation(dcm=np.eye(3)),
                 criterion.CableLength(
                     Standard(),
                     np.asarray([0.5, 1.5]) * np.sqrt(1)),
                 [-1.0],
                 [1.0],
                 9)) for rob in ([robots.robot_1t()])
        )
    )
    def test_render_linear_workspace(self,
                                     wizard: visualization.Visualizer,
                                     robot: Robot,
                                     ws_algorithm:
                                     workspace.workspace.Algorithm):
        # evaluate the workspace
        workspace = ws_algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(workspace)
        wizard.draw()
        wizard.show()

    @pytest.mark.parametrize(
        ('wizard', 'robot', 'ws_algorithm'),
        (
            (visualization.Visualizer(
                visualization.engine.plotly.Planar()),
             rob,
             workspace.grid.Algorithm(
                 archetype.Translation(dcm=np.eye(3)),
                 criterion.CableLength(
                     Standard(),
                     np.asarray([0.5, 1.5]) * np.sqrt(2)),
                 [-1.0, -1.0],
                 [1.0, 1.0],
                 9)) for rob in (robots.robot_2t(), robots.robot_1r2t())
        )
    )
    def test_render_planar_workspace(self,
                                     wizard: visualization.Visualizer,
                                     robot: Robot,
                                     ws_algorithm:
                                     workspace.workspace.Algorithm):
        # evaluate the workspace
        workspace = ws_algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(workspace)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
        ('wizard', 'robot', 'ws_algorithm'),
        (
            itertools.chain(
                ((visualization.Visualizer(
                    visualization.engine.plotly.Spatial()),
                  rob,
                  workspace.grid.Algorithm(
                          archetype.Translation(dcm=np.eye(3)),
                      criterion.CableLength(
                          Standard(),
                          np.asarray([0.5, 1.5]) * np.sqrt(3)),
                      [-1.0, -1.0, -1.0],
                      [1.0, 1.0, 1.0],
                      9)) for rob in
                (robots.robot_3t(), robots.robot_2r3t(), robots.robot_3r3t())),
                ((visualization.Visualizer(
                    visualization.engine.plotly.Spatial()),
                  rob,
                  workspace.hull.Algorithm(
                          archetype.Translation(dcm=np.eye(3)),
                      criterion.CableLength(
                          Standard(),
                          np.asarray([0.5, 1.5]) * np.sqrt(3)),
                      [0.0, 0.0, 0.0],
                      9)) for rob in
                (robots.robot_3t(), robots.robot_2r3t(), robots.robot_3r3t()))
            )
        )
    )
    def test_render_spatial_workspace(self,
                                      wizard: visualization.Visualizer,
                                      robot: Robot,
                                      ws_algorithm:
                                      workspace.workspace.Algorithm):
        # evaluate the workspace
        workspace = ws_algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(workspace)
        wizard.draw()
        wizard.show()
        wizard.close()


if __name__ == "__main__":
    pytest.main()
