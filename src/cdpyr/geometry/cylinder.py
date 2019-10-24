from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cylinder(Geometry):
    _diameter: float
    _height: float

    def __init__(self,
                 height: Optional[Num] = None,
                 diameter: Optional[Num] = None
                 ):
        self.height = height or 0
        self.diameter = diameter or 0

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: Num):
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
    def height(self, height: Num):
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
    def radius(self, radius: Num):
        if radius < 0:
            raise ValueError('radius must be nonnegative')
        self.diameter = 2.0 * radius

    @radius.deleter
    def radius(self):
        del self.diameter

    def moment_of_inertia(self):
        mass = self.mass
        r = self.radius
        h = self.height
        rh = 3.0 * (r ** 2.0) + h ** 2.0

        return 1.0 / 12.0 * mass * np_.asarray((
            rh,
            rh,
            6.0 * (r ** 2.0)
        ))


Cylinder.__repr__ = make_repr(
    'diameter',
    'height'
)

__all__ = [
    'Cylinder',
]
