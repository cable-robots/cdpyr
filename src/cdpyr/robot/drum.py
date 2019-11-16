from typing import Optional, Tuple, Union

from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.mechanics import inertia as _inertia
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Drum(BaseObject):
    _geometry: '_geometry.Geometry'
    _inertia: '_inertia.Inertia'

    def __init__(self,
                 geometry: Optional['_geometry.Geometry'] = None,
                 inertia: Optional[
                     Union[Tuple[Vector, Matrix], '_inertia.Inertia']] = None
                 ):
        self.geometry = geometry or _geometry.Geometry()
        self.inertia = inertia or _inertia.Inertia()

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, geometry: '_geometry.Geometry'):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self.geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                inertia: Union[Tuple[Vector, Matrix], '_inertia.Inertia']):
        if not isinstance(inertia, _inertia.Inertia):
            inertia = _inertia.Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self.inertia

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.geometry == other.geometry and \
               self.inertia == other.inertia

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
