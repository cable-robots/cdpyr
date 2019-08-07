from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np_
from magic_repr import make_repr

from .geometry import Geometry

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Tube(Geometry):
    _inner_diameter: float
    _outer_diameter: float
    _height: float

    def __init__(self,
                 inner_diameter: Optional[_TNum] = None,
                 outer_diameter: Optional[_TNum] = None,
                 height: Optional[_TNum] = None
                 ):
        self.inner_diameter = inner_diameter or 0
        self.outer_diameter = outer_diameter or 0
        self.height = height or 0

    @property
    def diameter(self):
        return self.inner_diameter, self.outer_diameter

    @diameter.setter
    def diameter(self, diameter: Tuple[_TNum, _TNum]):
        self.inner_diameter = diameter[0]
        self.outer_diameter = diameter[1]

    @diameter.deleter
    def diameter(self):
        del self.inner_diameter
        del self.outer_diameter

    @property
    def inner_diameter(self):
        return self._inner_diameter

    @inner_diameter.setter
    def inner_diameter(self, inner_diameter: _TNum):
        if inner_diameter < 0:
            raise ValueError('inner_diameter must be nonnegative')

        if self.outer_diameter < inner_diameter:
            raise ValueError('inner_diameter must be smaller than outer '
                             'diameter')
        self._inner_diameter = inner_diameter

    @inner_diameter.deleter
    def inner_diameter(self):
        del self._inner_diameter

    @property
    def outer_diameter(self):
        return self._outer_diameter

    @outer_diameter.setter
    def outer_diameter(self, outer_diameter: _TNum):
        if outer_diameter < 0:
            raise ValueError('outer_diameter must be nonnegative')

        if outer_diameter < self.inner_diameter:
            raise ValueError('outer_diameter must be larger than '
                             'inner_diameter')
        self._outer_diameter = outer_diameter

    @outer_diameter.deleter
    def outer_diameter(self):
        del self._outer_diameter

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
    def inner_radius(self):
        return self._inner_diameter / 2.0

    @inner_radius.setter
    def inner_radius(self, inner_radius: _TNum):
        if inner_radius < 0:
            raise ValueError('inner_radius must be nonnegative')
        self.inner_diameter = 2.0 * inner_radius

    @inner_radius.deleter
    def inner_radius(self):
        del self.inner_diameter

    @property
    def outer_radius(self):
        return self._outer_diameter / 2.0

    @outer_radius.setter
    def outer_radius(self, outer_radius: _TNum):
        if outer_radius < 0:
            raise ValueError('outer_radius must be nonnegative')
        self.outer_diameter = 2.0 * outer_radius

    @outer_radius.deleter
    def outer_radius(self):
        del self.outer_diameter

    def moment_of_inertia(self, mass: _TNum):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        ri = self.inner_radius
        ro = self.outer_radius
        r = (ri ** 2.0) + (ro ** 2.0)
        h = self.height
        rh = 3.0 * (r ** 2.0) + h ** 2.0

        return 1.0 / 12.0 * mass * np_.array((
            rh,
            rh,
            6.0 * (r ** 2.0)
        ))


Tube.__repr__ = make_repr(
    'inner_diameter',
    'outer_diameter',
    'height'
)

__all__ = ['Tube']
