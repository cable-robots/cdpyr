from typing import Optional, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.mechanics import inertia as _inertia
from cdpyr.typing import Matrix, Vector


class Pulley(object):
    _geometry: '_geometry.Geometry'
    _inertia: '_inertia.Inertia'
    _angular: '_angular.Angular'

    def __init__(self,
                 geometry: Optional['_geometry.Geometry'] = None,
                 inertia: Optional[
                     Union[Tuple[Vector, Matrix], '_inertia.Inertia']] = None,
                 dcm: Optional[Matrix] = None,
                 angular: Optional['_angular.Angular'] = None
                 ):
        self.geometry = geometry or _geometry.Geometry()
        self.inertia = inertia or _inertia.Inertia()
        if angular is None:
            self.angular = _angular.Angular(
                dcm=dcm if dcm is not None else np_.eye(3))
        else:
            self.angular = angular

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: '_geometry.Geometry'):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self._geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                inertia: Union[Tuple[Vector, Matrix], '_inertia.Inertia']):
        if not isinstance(inertia, _inertia.Inertia):
            inertia = _inertia.Inertia(inertia[0], inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: '_angular.Angular'):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self.angular

    @property
    def dcm(self):
        return self.angular.dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        self.angular.dcm = dcm


Pulley.__repr__ = make_repr(
    'geometry',
    'inertia',
    'angular'
)

__all__ = [
    'Pulley',
]
