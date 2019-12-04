import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cuboid(Geometry):
    width: float
    height: float
    depth: float

    def __init__(self, width: Num, depth: Num, height: Num, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.depth = depth

    def _calculate_centroid(self):
        return _np.zeros((3,))

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
