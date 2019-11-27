import pytest

from cdpyr import visualization
from cdpyr.geometry import Cylinder

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryCylinderTestSuite(object):

    def test_plot_planar_cylinder(self,
                                   tmpdir):
        # create a cylinder
        cylinder = Cylinder(1.00, 0.0)

        # and visualize
        visualizer = visualization.matplotlib.Planar()
        visualizer.render(cylinder)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()

    def test_plot_spatial_cylinder(self,
                                   tmpdir):
        # create a cylinder
        cylinder = Cylinder(1.00, 1.00)

        # and visualize
        visualizer = visualization.matplotlib.Spatial()
        visualizer.render(cylinder)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
