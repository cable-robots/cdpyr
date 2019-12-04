import itertools

import pytest

from cdpyr import visualization
from cdpyr.geometry import Cuboid, Cylinder, Ellipsoid, Tube
from cdpyr.geometry.primitive import Primitive

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlotRobotTestSuite(object):

    @pytest.mark.parametrize(
        ('engine', 'geometry'),
        itertools.product((visualization.engine.plotly.Linear,
                           visualization.engine.plotly.Planar,
                           visualization.engine.plotly.Spatial,),
                          (
                              Cuboid(1.00, 2.00, 3.0),
                              Cylinder(1.00, 2.00),
                              Cylinder([1.00, 2.00], 3.00),
                              Ellipsoid(1.00),
                              Ellipsoid([1.00, 2.00, 3.00]),
                              Tube(1.00, 2.00, 3.00),
                              Tube([1.00, 2.00], 3.00, 4.00),
                              Tube([1.00, 2.00], [3.00, 4.00], 5.00),
                          )
                          )
    )
    def test_render(self, engine: visualization.engine.Engine, geometry: Primitive):
        wizard = visualization.Visualizer(engine())
        wizard.render(geometry)
        wizard.draw()
        wizard.show()
        wizard.close()


if __name__ == "__main__":
    pytest.main()
