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
        visualizer = visualization.plotly.PLANAR()
        visualizer.render(cuboid)
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
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(cuboid)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
