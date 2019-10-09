from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num


class Sphere(Geometry):
    _diameter: float

    def __init__(self,
                 diameter: Optional[Num] = None,
                 ):
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
        rs = self.radius ** 2.0

        return 2.0 / 3.0 * mass * np_.array((
            rs,
            rs,
            rs
        ))


Sphere.__repr__ = make_repr(
    'diameter'
)

__all__ = [
    'Sphere',
]
