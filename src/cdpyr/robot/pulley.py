from typing import Optional, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.mechanics import inertia as _inertia
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pulley(BaseObject):
    angular: '_angular.Angular'
    geometry: '_geometry.Geometry'
    inertia: '_inertia.Inertia'

    def __init__(self,
                 geometry: Optional['_geometry.Geometry'] = None,
                 inertia: Optional['_inertia.Inertia'] = None,
                 dcm: Optional[Matrix] = None,
                 angular: Optional['_angular.Angular'] = None
                 ):
        self.geometry = geometry or _geometry.Geometry()
        self.inertia = inertia or _inertia.Inertia()
        if angular is None:
            angular = _angular.Angular(dcm=dcm if dcm is not None else np_.eye(3))
        self.angular = angular

    @property
    def dcm(self):
        return self.angular.dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        self.angular.dcm = dcm

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.angular == other.angular \
               and self.geometry == other.geometry \
               and self.inertia == other.inertia

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.angular, self.geometry, self.inertia))

    __repr__ = make_repr(
        'geometry',
        'inertia',
        'angular'
    )


__all__ = [
    'Pulley',
]
