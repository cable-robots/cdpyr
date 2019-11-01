from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


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
        _validator.numeric.nonnegative(width, 'width')

        self._width = width

    @width.deleter
    def width(self):
        del self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: Num):
        _validator.numeric.nonnegative(height, 'height')

        self._height = height

    @height.deleter
    def height(self):
        del self._height

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth: Num):
        _validator.numeric.nonnegative(depth, 'depth')

        self._depth = depth

    @depth.deleter
    def depth(self):
        del self._depth

    def moment_of_inertia(self):
        mass = self.mass
        w = self.width
        d = self.depth
        h = self.height

        return 1.0 / 12.0 * mass * np_.asarray((
            d ** 2.0 + h ** 2.0,
            w ** 2.0 + h ** 2.0,
            w ** 2.0 + d ** 2.0,
        ))


Cuboid.__repr__ = make_repr(
    'mass',
    'width',
    'depth',
    'height',
)

__all__ = [
    'Cuboid',
]
