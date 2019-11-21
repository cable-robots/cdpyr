import pytest

from cdpyr import visualization
from cdpyr.motion import Pose
from cdpyr.robot import Robot
from cdpyr.geometry import EllipticCylinder

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotGeometryEllipticCylinderTestSuite(object):

    def test_plot_spatial_elliptic_cylinder(self,
                             tmpdir):
        # create a cylinder
        elliptic_cylinder = EllipticCylinder(1.00, 0.25, 0.50)

        # and visualize
        visualizer = visualization.plotly.SPATIAL()
        visualizer.render(elliptic_cylinder)
        visualizer.draw()
        visualizer.show()
        # visualizer.figure.savefig(
        #     f'{tmpdir / sys._getframe().f_code.co_name}_empty')
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
