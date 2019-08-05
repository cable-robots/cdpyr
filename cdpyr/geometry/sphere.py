from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from .geometry import Geometry

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Sphere(Geometry):
    _diameter: float

    def __init__(self,
                 diameter: Optional[_TNum] = None,
                 ):
        self.diameter = diameter if diameter is not None else 0

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

        rs = self.radius ** 2.0

        return 2.0 / 3.0 * mass * np_.array((
            rs,
            rs,
            rs
        ))


Sphere.__repr__ = make_repr('diameter')

__all__ = ['Sphere']
