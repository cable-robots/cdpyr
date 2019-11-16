from typing import Optional, Tuple

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Tube(Geometry):
    _inner_diameter: float
    _outer_diameter: float
    _height: float

    def __init__(self,
                 inner_diameter: Optional[Num] = None,
                 outer_diameter: Optional[Num] = None,
                 height: Optional[Num] = None
                 ):
        self.inner_diameter = inner_diameter or 0
        self.outer_diameter = outer_diameter or 0
        self.height = height or 0

    @property
    def diameter(self):
        return self.inner_diameter, self.outer_diameter

    @diameter.setter
    def diameter(self, diameter: Tuple[Num, Num]):
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
    def inner_diameter(self, inner_diameter: Num):
        _validator.numeric.nonnegative(inner_diameter, 'inner_diameter')

        if self.outer_diameter:
            _validator.numeric.less_than(inner_diameter,
                                         self.outer_diameter,
                                         'inner_diameter')

        self._inner_diameter = inner_diameter

    @inner_diameter.deleter
    def inner_diameter(self):
        del self._inner_diameter

    @property
    def outer_diameter(self):
        return self._outer_diameter

    @outer_diameter.setter
    def outer_diameter(self, outer_diameter: Num):
        _validator.numeric.nonnegative(outer_diameter, 'outer_diameter')

        if self.inner_diameter:
            _validator.numeric.greater_than(outer_diameter,
                                            self.inner_diameter,
                                            'outer_diameter')

        self._outer_diameter = outer_diameter

    @outer_diameter.deleter
    def outer_diameter(self):
        del self._outer_diameter

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
    def inner_radius(self):
        return self._inner_diameter / 2.0

    @inner_radius.setter
    def inner_radius(self, inner_radius: Num):
        _validator.numeric.nonnegative(inner_radius, 'inner_radius')

        self.inner_diameter = 2.0 * inner_radius

    @inner_radius.deleter
    def inner_radius(self):
        del self.inner_diameter

    @property
    def outer_radius(self):
        return self._outer_diameter / 2.0

    @outer_radius.setter
    def outer_radius(self, outer_radius: Num):
        _validator.numeric.nonnegative(outer_radius, 'outer_radius')

        self.outer_diameter = 2.0 * outer_radius

    @outer_radius.deleter
    def outer_radius(self):
        del self.outer_diameter

    def moment_of_inertia(self):
        mass = self.mass
        ri = self.inner_radius
        ro = self.outer_radius
        r = (ri ** 2.0) + (ro ** 2.0)
        h = self.height
        rh = 3.0 * (r ** 2.0) + h ** 2.0

        return 1.0 / 12.0 * mass * np_.asarray((
            rh,
            rh,
            6.0 * (r ** 2.0)
        ))

    __repr__ = make_repr(
        'mass',
        'inner_diameter',
        'outer_diameter',
        'height',
    )


__all__ = [
    'Tube',
]
