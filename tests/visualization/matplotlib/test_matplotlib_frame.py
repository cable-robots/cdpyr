import sys

import pytest
from matplotlib import use

from cdpyr import visualization
from cdpyr.robot import Robot

if sys.platform == 'darwin':
    use('MacOSX')

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotPlatformTestSuite(object):

    def test_plot_frame_1t(self,
                           tmpdir,
                           robot_1t: Robot):
        visualizer = visualization.matplotlib.Linear()
        visualizer.render(robot_1t.frame)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_frame_2t(self,
                           tmpdir,
                           robot_2t: Robot):
        visualizer = visualization.matplotlib.Planar()
        visualizer.render(robot_2t.frame)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_frame_3t(self,
                           tmpdir,
                           robot_3t: Robot):
        visualizer = visualization.matplotlib.Spatial()
        visualizer.render(robot_3t.frame)
        visualizer.figure.axes[0].set_xlim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_zlim3d(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_frame_1r2t(self,
                             tmpdir,
                             robot_1r2t: Robot):
        visualizer = visualization.matplotlib.Planar()
        visualizer.render(robot_1r2t.frame)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_frame_2r3t(self,
                             tmpdir,
                             robot_2r3t: Robot):
        visualizer = visualization.matplotlib.Spatial()
        visualizer.render(robot_2r3t.frame)
        visualizer.figure.axes[0].set_xlim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_zlim3d(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_frame_3r3t(self,
                             tmpdir,
                             robot_3r3t: Robot):
        visualizer = visualization.matplotlib.Spatial()
        visualizer.render(robot_3r3t.frame)
        visualizer.figure.axes[0].set_xlim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim3d(-1.1, 1.1)
        visualizer.figure.axes[0].set_zlim3d(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        visualizer.figure.savefig(
            f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
