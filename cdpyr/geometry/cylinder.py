from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from .geometry import Geometry

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Cylinder(Geometry):
    _diameter: float
    _height: float

    def __init__(self,
                 height: Optional[_TNum] = None,
                 diameter: Optional[_TNum] = None
                 ):
        self.height = height or 0
        self.diameter = diameter or 0

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: _TNum):
        if diameter < 0:
            raise ValueError('diameter must be nonnegative')
        self._diameter = diameter

    @diameter.deleter
    def diameter(self):
        del self._diameter

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
    def radius(self):
        return self._diameter / 2.0

    @radius.setter
    def radius(self, radius: _TNum):
        if radius < 0:
            raise ValueError('radius must be nonnegative')
        self.diameter = 2.0 * radius

    @radius.deleter
    def radius(self):
        del self.diameter

    def moment_of_inertia(self, mass: _TNum):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        r = self.radius
        h = self.height
        rh = 3.0 * (r ** 2.0) + h ** 2.0

        return 1.0 / 12.0 * mass * np_.array((
            rh,
            rh,
            6.0 * (r ** 2.0)
        ))


Cylinder.__repr__ = make_repr(
    'diameter',
    'height'
)

__all__ = ['Cylinder']
