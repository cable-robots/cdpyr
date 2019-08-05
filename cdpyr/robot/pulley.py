from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry
from cdpyr.mechanics.inertia import Inertia
from cdpyr.mechanics.transformation.angular import Angular as AngularTransformation

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Pulley(object):
    _geometry: Geometry
    _inertia: Inertia
    _angular: AngularTransformation

    def __init__(self,
                 geometry: Optional[Geometry] = None,
                 inertia: Optional[Union[Tuple[Union[_TNum, _TVector], Union[
                     _TVector, _TMatrix]], Inertia]] = None,
                 rotation: Optional[
                     Union[_TMatrix, AngularTransformation]] = None
                 ):
        self.geometry = geometry if geometry is not None else Geometry()
        self.inertia = inertia if inertia is not None else Inertia()
        self.angular = rotation if rotation is not None else AngularTransformation()

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: Geometry):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self._geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self, inertia: Union[Tuple[_TVector, _TMatrix], Inertia]):
        if not isinstance(inertia, Inertia):
            inertia = Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: AngularTransformation):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self.angular


Pulley.__repr__ = make_repr('geometry', 'inertia', 'angular')

__all__ = ['Pulley']
