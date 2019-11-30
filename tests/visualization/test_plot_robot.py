import pytest

from cdpyr import robot, visualization
from cdpyr.motion.pose import pose

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"




class PlotRobotTestSuite(object):

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Linear())
            ]
    )
    def test_render_1t(self, engine: visualization.engine.Engine,
                       robot_1t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_1t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Linear())
            ]
    )
    def test_render_1t_random(self, engine: visualization.engine.Engine,
                              rand_pose_1t: pose.Pose,
                              robot_1t: robot.Robot):
        robot_1t.platforms[0].pose = rand_pose_1t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_1t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Planar())
            ]
    )
    def test_render_2t(self, engine: visualization.engine.Engine,
                       robot_2t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_2t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Planar())
            ]
    )
    def test_render_2t_random(self, engine: visualization.engine.Engine,
                              rand_pose_2t: pose.Pose,
                              robot_2t: robot.Robot):
        robot_2t.platforms[0].pose = rand_pose_2t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_2t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_3t(self, engine: visualization.engine.Engine,
                       robot_3t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_3t_random(self, engine: visualization.engine.Engine,
                              rand_pose_3t: pose.Pose,
                              robot_3t: robot.Robot):
        robot_3t.platforms[0].pose = rand_pose_3t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Planar())
            ]
    )
    def test_render_1r2t(self, engine: visualization.engine.Engine,
                         robot_1r2t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_1r2t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Planar())
            ]
    )
    def test_render_1r2t_random(self, engine: visualization.engine.Engine,
                                rand_pose_1r2t: pose.Pose,
                                robot_1r2t: robot.Robot):
        robot_1r2t.platforms[0].pose = rand_pose_1r2t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_1r2t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_2r3t(self, engine: visualization.engine.Engine,
                         robot_2r3t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_2r3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_2r3t_random(self, engine: visualization.engine.Engine,
                                rand_pose_2r3t: pose.Pose,
                                robot_2r3t: robot.Robot):
        robot_2r3t.platforms[0].pose = rand_pose_2r3t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_2r3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_3r3t(self, engine: visualization.engine.Engine,
                         robot_3r3t: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_3r3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_3r3t_random(self, engine: visualization.engine.Engine,
                                rand_pose_3r3t: pose.Pose,
                                robot_3r3t: robot.Robot):
        robot_3r3t.platforms[0].pose = rand_pose_3r3t
        wizard = visualization.Visualizer(engine)
        wizard.render(robot_3r3t)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_ipanema3(self, engine: visualization.engine.Engine,
                             ipanema_3: robot.Robot):
        wizard = visualization.Visualizer(engine)
        wizard.render(ipanema_3)
        wizard.draw()
        wizard.show()
        wizard.close()

    @pytest.mark.parametrize(
            ('engine'),
            [
                (visualization.engine.plotly.Spatial())
            ]
    )
    def test_render_ipanema3_random(self, engine: visualization.engine.Engine,
                                    rand_pose_3r3t: pose.Pose,
                                    ipanema_3: robot.Robot):
        ipanema_3.platforms[0].pose = rand_pose_3r3t
        wizard = visualization.Visualizer(engine)
        wizard.render(ipanema_3)
        wizard.draw()
        wizard.show()
        wizard.close()


if __name__ == "__main__":
    pytest.main()
