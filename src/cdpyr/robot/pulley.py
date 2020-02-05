from __future__ import annotations

from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry import primitive as _geometry
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.mechanics import inertia as _inertia
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pulley(RobotComponent):
    angular: _angular.Angular
    geometry: _geometry.Primitive
    inertia: _inertia.Inertia
    radius: Num

    def __init__(self,
                 radius: Num,
                 geometry: Optional[_geometry.Primitive] = None,
                 inertia: Optional[_inertia.Inertia] = None,
                 dcm: Optional[Matrix] = None,
                 angular: Optional[_angular.Angular] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.geometry = geometry or None
        self.inertia = inertia or _inertia.Inertia()
        if angular is None:
            angular = _angular.Angular(
                    dcm=dcm if dcm is not None else np_.eye(3))
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

        return self.radius == other.radius \
               and self.angular == other.angular \
               and self.geometry == other.geometry \
               and self.inertia == other.inertia

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.angular, self.geometry, self.inertia, self.radius))

    __repr__ = make_repr(
            'radius',
            'geometry',
            'inertia',
            'angular'
    )


__all__ = [
        'Pulley',
]
