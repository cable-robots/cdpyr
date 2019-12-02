from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cuboid(Geometry):
    width: float
    height: float
    depth: float

    def __init__(self,
                 width: Num,
                 depth: Num,
                 height: Num
                 ):
        self.width = width
        self.height = height
        self.depth = depth

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.width == other.width \
               and self.height == other.height \
               and self.depth == other.depth

    def __hash__(self):
        return hash((self.depth, self.height, self.width))

    __repr__ = make_repr(
            'width',
            'depth',
            'height',
    )


__all__ = [
        'Cuboid',
]
