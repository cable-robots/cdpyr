from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Cuboid(Geometry):
    _width: float
    _height: float
    _depth: float

    def __init__(self,
                 width: Optional[_TNum] = None,
                 height: Optional[_TNum] = None,
                 depth: Optional[_TNum] = None
                 ):
        self.width = width or 0
        self.height = height or 0
        self.depth = depth or 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: _TNum):
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
    def height(self, height: _TNum):
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
    def depth(self, depth: _TNum):
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

__all__ = ['Cuboid']
