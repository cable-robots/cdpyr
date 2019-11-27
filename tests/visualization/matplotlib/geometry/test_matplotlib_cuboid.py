import pytest

from cdpyr import visualization
from cdpyr.geometry import Cuboid

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryCuboidTestSuite(object):

    def test_plot_planar_cuboid(self,
                                tmpdir):
        # create a cuboid
        cuboid = Cuboid(1.0, 0.5, 0.25)

        # and visualize
        visualizer = visualization.matplotlib.Planar()
        visualizer.render(cuboid)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_spatial_cuboid(self,
                                 tmpdir):
        # create a cuboid
        cuboid = Cuboid(1.0, 0.5, 0.25)

        # and visualize
        visualizer = visualization.matplotlib.Spatial()
        visualizer.render(cuboid)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_linear_cuboid(self,
                                tmpdir):
        # create a cuboid
        cuboid = Cuboid(1.0, 0.5, 0.25)

        # and visualize
        visualizer = visualization.matplotlib.Linear()
        visualizer.render(cuboid)
        visualizer.figure.axes[0].set_xlim(-1.1, 1.1)
        visualizer.figure.axes[0].set_ylim(-1.1, 1.1)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
