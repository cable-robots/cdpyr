from __future__ import annotations

import itertools

import numpy as np
import pytest

from cdpyr import visualization
from cdpyr.analysis import archetype, criterion, workspace
from cdpyr.analysis.kinematics.standard import Standard
from cdpyr.analysis.workspace import workspace as _workspace
from cdpyr.geometry import Cuboid, Cylinder, Ellipsoid, Tube
from cdpyr.geometry.primitive import Primitive
from cdpyr.motion import pose
from cdpyr.robot import robot as _robot, sample as robots
from cdpyr.visualization.engine import engine as _engine, plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class VisualizationPlotlyTestSuite(object):

    @pytest.mark.parametrize(
            ('engine', 'geometry'),
            itertools.product((plotly.Linear(),
                               plotly.Planar(),
                               plotly.Spatial(),),
                              (
                                      Cuboid(1.00, 2.00, 3.0),
                                      Cylinder(1.00, 2.00),
                                      Cylinder([1.00, 2.00], 3.00),
                                      Ellipsoid(1.00),
                                      Ellipsoid([1.00, 2.00, 3.00]),
                                      Tube(1.00, 2.00, 3.00),
                                      Tube([1.00, 2.00], 3.00, 4.00),
                                      Tube([1.00, 2.00], [3.00, 4.00], 5.00),
                              )
                              )
    )
    def test_render(self,
                    engine: _engine.Engine,
                    geometry: Primitive):
        wizard = visualization.Visualizer(engine)
        wizard.render(geometry)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Linear(),),
            ]
    )
    def test_render_1t(self, engine: _engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_1t: _robot.Robot):
        robot = robot_1t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Linear(),),
            ]
    )
    def test_render_1t_random(self, engine: _engine.Engine,
                              ik_standard: Standard,
                              rand_pose_1t: pose.Pose,
                              robot_1t: _robot.Robot):
        robot = robot_1t
        pose = rand_pose_1t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Planar(),),
            ]
    )
    def test_render_2t(self, engine: _engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_2t: _robot.Robot):
        robot = robot_2t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Planar(),),
            ]
    )
    def test_render_2t_random(self, engine: _engine.Engine,
                              ik_standard: Standard,
                              rand_pose_2t: pose.Pose,
                              robot_2t: _robot.Robot):
        robot = robot_2t
        pose = rand_pose_2t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_3t(self, engine: _engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_3t: _robot.Robot):
        robot = robot_3t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_3t_random(self, engine: _engine.Engine,
                              ik_standard: Standard,
                              rand_pose_3t: pose.Pose,
                              robot_3t: _robot.Robot):
        robot = robot_3t
        pose = rand_pose_3t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Planar(),),
            ]
    )
    def test_render_1r2t(self, engine: _engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_1r2t: _robot.Robot):
        robot = robot_1r2t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Planar(),),
            ]
    )
    def test_render_1r2t_random(self, engine: _engine.Engine,
                                ik_standard: Standard,
                                rand_pose_1r2t: pose.Pose,
                                robot_1r2t: _robot.Robot):
        robot = robot_1r2t
        pose = rand_pose_1r2t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_2r3t(self, engine: _engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_2r3t: _robot.Robot):
        robot = robot_2r3t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_2r3t_random(self, engine: _engine.Engine,
                                ik_standard: Standard,
                                rand_pose_2r3t: pose.Pose,
                                robot_2r3t: _robot.Robot):
        robot = robot_2r3t
        pose = rand_pose_2r3t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_3r3t(self, engine: _engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_3r3t: _robot.Robot):
        robot = robot_3r3t
        pose = zero_pose

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_3r3t_random(self, engine: _engine.Engine,
                                ik_standard: Standard,
                                rand_pose_3r3t: pose.Pose,
                                robot_3r3t: _robot.Robot):
        robot = robot_3r3t
        pose = rand_pose_3r3t

        kinematics = ik_standard.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_ipanema3(self, engine: _engine.Engine,
                             ik_pulley: Standard,
                             zero_pose: pose.Pose,
                             ipanema_3: _robot.Robot):
        robot = ipanema_3
        pose = zero_pose

        kinematics = ik_pulley.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (plotly.Spatial(),),
            ]
    )
    def test_render_ipanema3_random(self, engine: _engine.Engine,
                                    ik_pulley: Standard,
                                    rand_pose_3r3t: pose.Pose,
                                    ipanema_3: _robot.Robot):
        robot = ipanema_3
        pose = rand_pose_3r3t

        kinematics = ik_pulley.backward(robot, pose)
        robot.platforms[0].pose = pose
        wizard = visualization.Visualizer(engine)
        wizard.render(robot)
        wizard.render(kinematics)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('wizard', 'robot', 'algorithm'),
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
                                     robot: _robot.Robot,
                                     algorithm: _workspace.Algorithm):
        # evaluate the workspace
        ws = algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(ws)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('wizard', 'robot', 'algorithm'),
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
                             9)) for rob in
                    (robots.robot_2t(), robots.robot_1r2t())
            )
    )
    def test_render_planar_workspace(self,
                                     wizard: visualization.Visualizer,
                                     robot: _robot.Robot,
                                     algorithm: _workspace.Algorithm):
        # evaluate the workspace
        ws = algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(ws)
        wizard.draw()
        # wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('wizard', 'robot', 'algorithm'),
            (
                    itertools.chain(
                            ((visualization.Visualizer(
                                    visualization.engine.plotly.Spatial()),
                              rob,
                              workspace.grid.Algorithm(
                                      archetype.Translation(dcm=np.eye(3)),
                                      criterion.CableLength(
                                              Standard(),
                                              np.asarray([0.5, 1.5]) * np.sqrt(
                                                      3)),
                                      [-1.0, -1.0, -1.0],
                                      [1.0, 1.0, 1.0],
                                      9)) for rob in
                                    (robots.robot_3t(), robots.robot_2r3t(),
                                     robots.robot_3r3t())),
                            ((visualization.Visualizer(
                                    visualization.engine.plotly.Spatial()),
                              rob,
                              workspace.hull.Algorithm(
                                      archetype.Translation(dcm=np.eye(3)),
                                      criterion.CableLength(
                                              Standard(),
                                              np.asarray([0.5, 1.5]) * np.sqrt(
                                                      3)),
                                      [0.0, 0.0, 0.0],
                                      9)) for rob in
                                    (robots.robot_3t(), robots.robot_2r3t(),
                                     robots.robot_3r3t()))
                    )
            )
    )
    def test_render_spatial_workspace(self,
                                      wizard: visualization.Visualizer,
                                      robot: _robot.Robot,
                                      algorithm: _workspace.Algorithm):
        # evaluate the workspace
        ws = algorithm.evaluate(robot)

        # visualize the result
        wizard.render(robot)
        wizard.render(ws)
        wizard.draw()
        # wizard.show()
        wizard.close()


if __name__ == "__main__":
    pytest.main()
