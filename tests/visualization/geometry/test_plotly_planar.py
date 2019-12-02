import pytest

from cdpyr import geometry
from cdpyr import (
    visualization
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotlyGeometryTestSuite(object):

    @pytest.mark.parametrize(
        ('shape'),
        (
                (geometry.Cuboid(1.0, 2.0, 3.0)),
                (geometry.Cylinder(1.0, 2.0)),
                (geometry.EllipticCylinder(1.0, 2.0, 3.0)),
                (geometry.Sphere(1.0)),
                (geometry.Tube(1.0, 2.0, 3.0))
        )
    )
    def test_plot_planar(self, shape: geometry.Geometry):
        visualizer = visualization.plotly.Planar()
        visualizer.render(shape)
        visualizer.draw()
        visualizer.show()
        visualizer.close()


if __name__ == "__main__":
    pytest.main()
