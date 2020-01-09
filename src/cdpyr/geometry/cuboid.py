import numpy as _np
from cached_property import cached_property
from magic_repr import make_repr
from scipy.spatial import Delaunay as _Delaunay

import numpy as _np

from cdpyr.geometry.primitive import Primitive
from cdpyr.typing import Num, Vector

from scipy.spatial import Delaunay as _Delaunay

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cuboid(Primitive):
    width: float
    height: float
    depth: float

    def __init__(self, width: Num, depth: Num, height: Num,
                 center: Vector = None,
                 **kwargs):
        super().__init__(center, **kwargs)
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def centroid(self):
        return self.center

    @property
    def corners(self):
        return _np.asarray((
                (-0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5),
                (0.5, -0.5, 0.5),
                (-0.5, -0.5, 0.5),
                (-0.5, 0.5, -0.5),
                (0.5, 0.5, -0.5),
                (0.5, -0.5, -0.5),
                (-0.5, -0.5, -0.5),
        )) * (self.width, self.depth, self.height) + self._center

    @property
    def faces(self):
        return _Delaunay(self.corners).convex_hull

    @property
    def vertices(self):
        return _Delaunay(self.corners).points

    @property
    def surface_area(self):
        # more readable access to often used variables
        w, d, h = self.width, self.depth, self.height

        return 2 * (w * d + d * h + w * h)

    @property
    def volume(self):
        return self.width * self.depth * self.height

    __repr__ = make_repr(
            'width',
            'depth',
            'height',
    )


__all__ = [
        'Cuboid',
]
