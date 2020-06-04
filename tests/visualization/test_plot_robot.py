from __future__ import annotations

import pytest

from cdpyr import robot, visualization
from cdpyr.analysis.kinematics.standard import Standard
from cdpyr.motion import pose

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotRobotTestSuite(object):

    @pytest.mark.parametrize(
            ('engine',),
            [
                    (visualization.engine.plotly.Linear(),),
            ]
    )
    def test_render_1t(self, engine: visualization.engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_1t: robot.Robot):
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
                    (visualization.engine.plotly.Linear(),),
            ]
    )
    def test_render_1t_random(self, engine: visualization.engine.Engine,
                              ik_standard: Standard,
                              rand_pose_1t: pose.Pose,
                              robot_1t: robot.Robot):
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
                    (visualization.engine.plotly.Planar(),),
            ]
    )
    def test_render_2t(self, engine: visualization.engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_2t: robot.Robot):
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
                    (visualization.engine.plotly.Planar(),),
            ]
    )
    def test_render_2t_random(self, engine: visualization.engine.Engine,
                              ik_standard: Standard,
                              rand_pose_2t: pose.Pose,
                              robot_2t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
            ]
    )
    def test_render_3t(self, engine: visualization.engine.Engine,
                       ik_standard: Standard,
                       zero_pose: pose.Pose,
                       robot_3t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
            ]
    )
    def test_render_3t_random(self, engine: visualization.engine.Engine,
                              ik_standard: Standard,
                              rand_pose_3t: pose.Pose,
                              robot_3t: robot.Robot):
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
                    (visualization.engine.plotly.Planar(),),
            ]
    )
    def test_render_1r2t(self, engine: visualization.engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_1r2t: robot.Robot):
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
                    (visualization.engine.plotly.Planar(),),
            ]
    )
    def test_render_1r2t_random(self, engine: visualization.engine.Engine,
                                ik_standard: Standard,
                                rand_pose_1r2t: pose.Pose,
                                robot_1r2t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_2r3t(self, engine: visualization.engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_2r3t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_2r3t_random(self, engine: visualization.engine.Engine,
                                ik_standard: Standard,
                                rand_pose_2r3t: pose.Pose,
                                robot_2r3t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_3r3t(self, engine: visualization.engine.Engine,
                         ik_standard: Standard,
                         zero_pose: pose.Pose,
                         robot_3r3t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_3r3t_random(self, engine: visualization.engine.Engine,
                                ik_standard: Standard,
                                rand_pose_3r3t: pose.Pose,
                                robot_3r3t: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_ipanema3(self, engine: visualization.engine.Engine,
                             ik_pulley: Standard,
                             zero_pose: pose.Pose,
                             ipanema_3: robot.Robot):
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
                    (visualization.engine.plotly.Spatial(),),
                    (visualization.engine.mayavi.Spatial(),),
            ]
    )
    def test_render_ipanema3_random(self, engine: visualization.engine.Engine,
                                    ik_pulley: Standard,
                                    rand_pose_3r3t: pose.Pose,
                                    ipanema_3: robot.Robot):
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


if __name__ == "__main__":
    pytest.main()
