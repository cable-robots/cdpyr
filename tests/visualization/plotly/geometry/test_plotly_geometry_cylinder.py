import pytest

from cdpyr import visualization
from cdpyr.motion import Pose
from cdpyr.robot import Robot
from cdpyr.geometry import Cylinder

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryCylinderTestSuite(object):

    def test_plot_spatial_cylinder(self,
                             tmpdir):
        # create a cylinder
        cylinder = Cylinder(1.00, 1.00)

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
