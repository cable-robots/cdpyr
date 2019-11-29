from typing import Optional, Tuple, Union

from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.mechanics import inertia as _inertia
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Drum(BaseObject):
    geometry: '_geometry.Geometry'
    inertia: '_inertia.Inertia'

    def __init__(self,
                 geometry: Optional['_geometry.Geometry'] = None,
                 inertia: Optional['_inertia.Inertia'] = None
                 ):
        self.geometry = geometry or _geometry.Geometry()
        self.inertia = inertia or _inertia.Inertia()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.geometry == other.geometry \
               and self.inertia == other.inertia

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.geometry, self.inertia))

    __repr__ = make_repr(
        'geometry',
        'inertia'
    )


__all__ = [
    'Drum',
]
