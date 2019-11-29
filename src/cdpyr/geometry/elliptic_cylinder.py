from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class EllipticCylinder(Geometry):
    major_diameter: float
    minor_diameter: float
    height: float

    def __init__(self,
                 major_diameter: Num,
                 minor_diameter: Num,
                 height: Num,
                 ):
        self.major_diameter = major_diameter
        self.minor_diameter = minor_diameter
        self.height = height

    @property
    def major_radius(self):
        return self.major_diameter / 2.0

    @major_radius.setter
    def major_radius(self, radius: Num):
        self.major_diameter = 2.0 * radius

    @major_radius.deleter
    def major_radius(self):
        del self.major_diameter

    @property
    def minor_radius(self):
        return self.minor_diameter / 2.0

    @minor_radius.setter
    def minor_radius(self, radius: Num):
        self.minor_diameter = 2.0 * radius

    @minor_radius.deleter
    def minor_radius(self):
        del self.minor_diameter

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.major_diameter == other.major_diameter \
               and self.minor_diameter == other.minor_diameter \
               and self.height == other.height

    def __hash__(self):
        return hash((self.height, self.major_diameter, self.minor_diameter))

    __repr__ = make_repr(
        'major_diameter',
        'minor_diameter',
        'height',
    )


__all__ = [
    'EllipticCylinder',
]
