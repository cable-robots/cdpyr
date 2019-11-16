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
                 mass: Num,
                 width: Num,
                 height: Num,
                 depth: Num
                 ):
        super().__init__(mass)
        self.width = width
        self.height = height
        self.depth = depth

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

    def inertia(self):
        mass = self.mass
        w = self.width
        d = self.depth
        h = self.height

        return 1.0 / 12.0 * mass * np_.asarray((
            d ** 2.0 + h ** 2.0,
            w ** 2.0 + h ** 2.0,
            w ** 2.0 + d ** 2.0,
        ))

    __repr__ = make_repr(
        'mass',
        'width',
        'depth',
        'height',
    )


__all__ = [
    'Cuboid',
]
