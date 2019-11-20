import pytest

from cdpyr import visualization
from cdpyr.motion import Pose
from cdpyr.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotRobotTestSuite(object):

    def test_plot_robot_1t(self,
                           tmpdir,
                           robot_1t: Robot,
                           rand_pose_1t: Pose):
        visualizer = visualization.plotly.LINEAR()
        visualizer.render(robot_1t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_1t.platforms[0].pose = rand_pose_1t

        visualizer = visualization.plotly.LINEAR()
        visualizer.render(robot_1t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()

    def test_plot_robot_2t(self,
                           tmpdir,
                           robot_2t: Robot,
                           rand_pose_2t: Pose):
        visualizer = visualization.plotly.PLANAR()
        visualizer.render(robot_2t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_2t.platforms[0].pose = rand_pose_2t

        visualizer = visualization.plotly.PLANAR()
        visualizer.render(robot_2t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()

    def test_plot_robot_3t(self,
                           tmpdir,
                           robot_3t: Robot,
                           rand_pose_3t: Pose):
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_3t.platforms[0].pose = rand_pose_3t

        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()

    def test_plot_robot_1r2t(self,
                             tmpdir,
                             robot_1r2t: Robot,
                             rand_pose_1r2t: Pose):
        visualizer = visualization.plotly.PLANAR()
        visualizer.render(robot_1r2t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_1r2t.platforms[0].pose = rand_pose_1r2t

        visualizer = visualization.plotly.PLANAR()
        visualizer.render(robot_1r2t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()

    def test_plot_robot_2r3t(self,
                             tmpdir,
                             robot_2r3t: Robot,
                             rand_pose_2r3t: Pose):
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_2r3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_2r3t.platforms[0].pose = rand_pose_2r3t

        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_2r3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()

    def test_plot_robot_3r3t(self,
                             tmpdir,
                             robot_3r3t: Robot,
                             rand_pose_3r3t: Pose):
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_3r3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

        robot_3r3t.platforms[0].pose = rand_pose_3r3t

        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(robot_3r3t)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_random')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
