import itertools

import pytest

from cdpyr import visualization
from cdpyr.geometry import (
    Cuboid,
    Geometry
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotRobotTestSuite(object):

    @pytest.mark.parametrize(
        ('engine', 'geometry'),
        itertools.product((visualization.engine.plotly.Linear(),
                           visualization.engine.plotly.Planar(),
                           visualization.engine.plotly.Spatial()),
                          (
                              # Cylinder(1.00, 2.00),
                              Cuboid(1.00, 2.00, 3.0),
                              # EllipticCylinder(1.00, 2.00, 3.00),
                              # Tube(1.00, 2.00, 3.00),
                              # Sphere(1.00))
                          )
                          )
    )
    def test_render(self, geometry: Geometry,
                    engine: visualization.engine.Engine):
        wizard = visualization.Visualizer(engine)
        wizard.render(geometry)
        wizard.draw()
        wizard.show()
        wizard.close()


if __name__ == "__main__":
    pytest.main()
