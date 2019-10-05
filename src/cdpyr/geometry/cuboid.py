from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typedef import Num


class Cuboid(Geometry):
    _width: float
    _height: float
    _depth: float

    def __init__(self,
                 width: Optional[Num] = None,
                 height: Optional[Num] = None,
                 depth: Optional[Num] = None
                 ):
        self.width = width or 0
        self.height = height or 0
        self.depth = depth or 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: Num):
        if width < 0:
            raise ValueError('width must be nonnegative')
        self._width = width

    @width.deleter
    def width(self):
        del self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: Num):
        if height < 0:
            raise ValueError('height must be nonnegative')
        self._height = height

    @height.deleter
    def height(self):
        del self._height

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth: Num):
        if depth < 0:
            raise ValueError('depth must be nonnegative')
        self._depth = depth

    @depth.deleter
    def depth(self):
        del self._depth

    def moment_of_inertia(self):
        mass = self.mass
        w = self.width
        d = self.depth
        h = self.height

        return 1.0 / 12.0 * mass * np_.array((
            d ** 2.0 + h ** 2.0,
            w ** 2.0 + h ** 2.0,
            w ** 2.0 + d ** 2.0,
        ))


Cuboid.__repr__ = make_repr(
    'width',
    'depth',
    'height'
)

__all__ = [
    'Cuboid',
]
