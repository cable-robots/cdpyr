from typing import Tuple

from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Tube(Geometry):
    inner_diameter: float
    outer_diameter: float
    height: float

    def __init__(self,
                 inner_diameter: Num,
                 outer_diameter: Num,
                 height: Num
                 ):
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.height = height

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
    def inner_radius(self):
        return self.inner_diameter / 2.0

    @inner_radius.setter
    def inner_radius(self, inner_radius: Num):
        self.inner_diameter = 2.0 * inner_radius

    @inner_radius.deleter
    def inner_radius(self):
        del self.inner_diameter

    @property
    def outer_radius(self):
        return self.outer_diameter / 2.0

    @outer_radius.setter
    def outer_radius(self, outer_radius: Num):
        self.outer_diameter = 2.0 * outer_radius

    @outer_radius.deleter
    def outer_radius(self):
        del self.outer_diameter

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return super().__eq__(other) \
               and self.inner_diameter == other.inner_diameter \
               and self.outer_diameter == other.outer_diameter \
               and self.height == other.height

    def __hash__(self):
        return hash((self.height, self.inner_diameter, self.outer_diameter))

    __repr__ = make_repr(
            'inner_diameter',
            'outer_diameter',
            'height',
    )


__all__ = [
        'Tube',
]
