from __future__ import annotations

from typing import Mapping

import numpy as _np
import pytest

from cdpyr import geometry
from cdpyr.geometry.primitive import Primitive

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GeometryTestSuite(object):

    @pytest.mark.parametrize(
            ('geometry', 'expected'),
            (
                    (
                            geometry.Cuboid(1, 2, 3),
                            {'surface': 22,
                             'volume':  6,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Cuboid(1, 2, 3, [-1, -1, -1]),
                            {'surface': 22,
                             'volume':  6,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Cylinder(1, 2),
                            {'surface': 18.849555921539,
                             'volume':  6.2831853071796,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Cylinder(1, 2, [-1, -1, -1]),
                            {'surface': 18.849555921539,
                             'volume':  6.2831853071796,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Cylinder([1, 2], 3),
                            {'surface': 41.631715276002,
                             'volume':  18.849555921539,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Cylinder([1, 2], 3, [-1, -1, -1]),
                            {'surface': 41.631715276002,
                             'volume':  18.849555921539,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Ellipsoid(1),
                            {'surface': 12.56637061435917295385,
                             'volume':  4.188790204786390984617,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Ellipsoid(1, [-1, -1, -1]),
                            {'surface': 12.56637061435917295385,
                             'volume':  4.188790204786390984617,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Ellipsoid([1, 2, 3]),
                            {'surface': 48.8821463025820596957,
                             'volume':  25.1327412287183459077,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Ellipsoid([1, 2, 3], [-1, -1, -1]),
                            {'surface': 48.8821463025820596957,
                             'volume':  25.1327412287183459077,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Tube(1, 2, 3),
                            {'surface': 75.398223686156,
                             'volume':  28.2743338823086,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Tube(1, 2, 3, [-1, -1, -1]),
                            {'surface': 75.398223686156,
                             'volume':  28.2743338823086,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Tube([1, 2], 3, 4),
                            {'surface': 158.13431371860202,
                             'volume':  87.96459430051199,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Tube([1, 2], 3, 4, [-1, -1, -1]),
                            {'surface': 158.13431371860202,
                             'volume':  87.96459430051199,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
                    (
                            geometry.Tube([1, 2], [3, 4], 5),
                            {'surface': 221.791554978078,
                             'volume':  157.079632679492,
                             'center': [0, 0, 0],
                             'centroid': [0, 0, 0]}),
                    (
                            geometry.Tube([1, 2], [3, 4], 5, [-1, -1, -1]),
                            {'surface': 221.791554978078,
                             'volume':  157.079632679492,
                             'center': [-1, -1, -1],
                             'centroid': [-1, -1, -1]}),
            )
    )
    def test_surfaces(self, geometry: Primitive, expected: Mapping):
        assert geometry.center == pytest.approx(expected['center'])
        assert geometry.centroid == pytest.approx(expected['centroid'])
        assert geometry.surface_area == pytest.approx(expected['surface'], rel=1e-2)
        assert geometry.volume == pytest.approx(expected['volume'], rel=1e-2)


if __name__ == "__main__":
    pytest.main()
