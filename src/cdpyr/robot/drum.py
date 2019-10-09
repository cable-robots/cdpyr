from typing import Optional, Tuple, Union

from magic_repr import make_repr

from cdpyr.geometry import geometry as __geometry
from cdpyr.mechanics import inertia as __inertia
from cdpyr.typing import Matrix, Num, Vector


class Drum(object):
    _geometry: '__geometry.Geometry'
    _inertia: '__inertia.Inertia'

    def __init__(self,
                 geometry: Optional['__geometry.Geometry'] = None,
                 inertia: Optional[Union[Tuple[Union[Num, Vector], Union[
                     Vector, Matrix]], '__inertia.Inertia']] = None
                 ):
        self.geometry = geometry or __geometry.Geometry()
        self.inertia = inertia or __inertia.Inertia()

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, geometry: '__geometry.Geometry'):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self.geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                inertia: Union[Tuple[Union[Num, Vector], Union[
                    Vector, Matrix]], '__inertia.Inertia']):
        if not isinstance(inertia, __inertia.Inertia):
            inertia = __inertia.Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self.inertia


Drum.__repr__ = make_repr(
    'geometry',
    'inertia'
)

__all__ = [
    'Drum',
]
