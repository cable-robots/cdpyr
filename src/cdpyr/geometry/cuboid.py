import numpy as _np
from cached_property import cached_property
from magic_repr import make_repr
from scipy.spatial import Delaunay as _Delaunay

from cdpyr.geometry.primitive import Primitive
from cdpyr.typing import Num, Vector

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

    @cached_property
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
        )) * _np.asarray((self.width, self.depth, self.height)) + self.center

    @cached_property
    def faces(self):
        return _Delaunay(self.corners).convex_hull

    @cached_property
    def vertices(self):
        return _Delaunay(self.corners).points

    def _calculate_surface(self):
        # more readable access to often used variables
        w, d, h = self.width, self.depth, self.height

        return 2 * (w * d + d * h + w * h)

    def _calculate_volume(self):
        return self.width * self.depth * self.height

    __repr__ = make_repr(
            'width',
            'depth',
            'height',
    )


__all__ = [
        'Cuboid',
]
