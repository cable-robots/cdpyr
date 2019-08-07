from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.mechanics.inertia import Inertia

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Drum(object):
    _geometry: Geometry
    _inertia: Inertia

    def __init__(self,
                 geometry: Optional[Geometry] = None,
                 inertia: Optional[Union[Tuple[Union[_TNum, _TVector], Union[
                     _TVector, _TMatrix]], Inertia]] = None
                 ):

        self.geometry = geometry or Geometry()
        self.inertia = inertia or Inertia()

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, geometry: Geometry):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self.geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self, inertia: Union[
        Tuple[Union[_TNum, _TVector], Union[_TVector, _TMatrix]], Inertia]):
        if not isinstance(inertia, Inertia):
            inertia = Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self.inertia


Drum.__repr__ = make_repr(
    'geometry',
    'inertia'
)

__all__ = ['Drum']
