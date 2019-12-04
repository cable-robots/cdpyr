import numpy as _np
import pytest

from cdpyr import geometry
from cdpyr.geometry.geometry import Geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GeometryTestSuite(object):

    @pytest.mark.parametrize(
            ('geometry', 'expected'),
            (
                    (  # 0
                            geometry.Cuboid(1, 2, 3),
                            {'surface': 22,
                             'volume':  6}),
                    (  # 1
                            geometry.Cylinder(1, 2),
                            {'surface': 18.849555921539,
                             'volume':  6.2831853071796}),
                    (  # 2
                            geometry.Cylinder([1, 2], 3),
                            {'surface': 41.631715276002,
                             'volume':  18.849555921539}),
                    (  # 3
                            geometry.Ellipsoid(1),
                            {'surface': 12.56637061435917295385,
                             'volume':  4.188790204786390984617}),
                    (  # 4
                            geometry.Ellipsoid([1, 2, 3]),
                            {'surface': 48.8821463025820596957,
                             'volume':  25.1327412287183459077}),
                    (  # 5
                            geometry.Tube(1, 2, 3),
                            {'surface': 62.831853071796 -
                                        25.132741228718 + 2 *
                                        18.849555921539,
                             'volume':  37.699111843078 -
                                        9.4247779607694}),
                    (  # 6
                            geometry.Tube([1, 2], 3, 4),
                            {'surface': 131.94689145077 -
                                        51.32016349655 + 2 *
                                        38.753792882191,
                             'volume':  113.09733552923 -
                                        25.132741228718}),
                    (  # 7
                            geometry.Tube([1, 2], [3, 4], 5),
                            {'surface': 185.9156844897 -
                                        61.008611717098 + 2 *
                                        48.442241102738,
                             'volume':  188.49555921539 -
                                        31.415926535898}),
            )
    )
    def test_surfaces(self, geometry: Geometry, expected: dict):
        assert geometry.centroid == pytest.approx(_np.zeros((3,)))
        assert geometry.surface == pytest.approx(expected['surface'], rel=1e-2)
        assert geometry.volume == pytest.approx(expected['volume'], rel=1e-2)


if __name__ == "__main__":
    pytest.main()
