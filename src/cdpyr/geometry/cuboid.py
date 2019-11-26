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
                 width: Num,
                 depth: Num,
                 height: Num
                 ):
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

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.width == other.width \
               and self.height == other.height \
               and self.depth == other.depth

    def __hash__(self):
        return hash((self.depth, self.height, self.width))

    __repr__ = make_repr(
        'width',
        'depth',
        'height',
    )


__all__ = [
    'Cuboid',
]
