import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cylinder(Geometry):
    _diameter: float
    _height: float

    def __init__(self,
                 mass: Num,
                 height: Num,
                 diameter: Num
                 ):
        super().__init__(mass)
        self.height = height
        self.diameter = diameter

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: Num):
        _validator.numeric.nonnegative(diameter, 'diameter')

        self._diameter = diameter

    @diameter.deleter
    def diameter(self):
        del self._diameter

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
    def radius(self):
        return self._diameter / 2.0

    @radius.setter
    def radius(self, radius: Num):
        _validator.numeric.nonnegative(radius, 'radius')

        self.diameter = 2.0 * radius

    @radius.deleter
    def radius(self):
        del self.diameter

    def inertia(self):
        mass = self.mass
        r = self.radius
        h = self.height
        rh = 3.0 * (r ** 2.0) + h ** 2.0

        return 1.0 / 12.0 * mass * np_.asarray((
            rh,
            rh,
            6.0 * (r ** 2.0)
        ))

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.diameter == other.diameter and \
               self.height == other.height

    def __hash__(self):
        return hash((self.diameter, self.height, self.mass))

    __repr__ = make_repr(
        'mass',
        'diameter',
        'height',
    )


__all__ = [
    'Cylinder',
]
