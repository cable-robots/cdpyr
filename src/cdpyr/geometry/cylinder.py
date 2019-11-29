from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cylinder(Geometry):
    diameter: float
    height: float

    def __init__(self,
                 diameter: Num,
                 height: Num
                 ):
        self.diameter = diameter
        self.height = height

    @property
    def radius(self):
        return self.diameter / 2.0

    @radius.setter
    def radius(self, radius: Num):
        self.diameter = 2.0 * radius

    @radius.deleter
    def radius(self):
        del self.diameter

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.diameter == other.diameter \
               and self.height == other.height

    def __hash__(self):
        return hash((self.diameter, self.height))

    __repr__ = make_repr(
        'diameter',
        'height',
    )


__all__ = [
    'Cylinder',
]
