import pytest

from cdpyr import visualization
from cdpyr.geometry import Sphere

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryTubeTestSuite(object):

    def test_plot_linear_sphere(self,
                                 tmpdir):
        # create a sphere
        sphere = Sphere(1.00)

        # and visualize
        visualizer = visualization.plotly.Planar()
        visualizer.render(sphere)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_planar_sphere(self,
                                 tmpdir):
        # create a sphere
        sphere = Sphere(1.00)

        # and visualize
        visualizer = visualization.plotly.Planar()
        visualizer.render(sphere)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_spatial_sphere(self,
                                 tmpdir):
        # create a sphere
        sphere = Sphere(1.00)

        # and visualize
        visualizer = visualization.plotly.Spatial()
        visualizer.render(sphere)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
