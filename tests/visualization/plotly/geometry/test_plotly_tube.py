import pytest

from cdpyr import visualization
from cdpyr.geometry import Tube

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryTubeTestSuite(object):

    def test_plot_planar_tube(self,
                              tmpdir):
        # create a cylinder
        cylinder = Tube(0.50, 1.00, 1.00)

        # and visualize
        visualizer = visualization.plotly.PLANAR()
        visualizer.render(cylinder)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_spatial_tube(self,
                               tmpdir):
        # create a cylinder
        cylinder = Tube(0.50, 1.00, 1.00)

        # and visualize
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(cylinder)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
