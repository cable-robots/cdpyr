from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Inertia(BaseObject):
    _linear: np_.ndarray
    _angular: np_.ndarray

    def __init__(self,
                 linear: Optional[Matrix] = None,
                 angular: Optional[Matrix] = None
                 ):
        self.linear = linear if linear is not None else np_.diag(
                np_.full((3,), np_.inf))
        self.angular = angular if angular is not None else np_.diag(
                np_.full((3,), np_.inf))

    @staticmethod
    def cuboid(mass: Num, width: Num, depth: Num, height: Num):
        return Inertia(
                mass * np_.eye(3),
                1.0 / 12.0 * mass * np_.diag((
                        depth ** 2.0 + height ** 2.0,
                        width ** 2.0 + height ** 2.0,
                        width ** 2.0 + depth ** 2.0,
                ))
        )

    @staticmethod
    def cylinder(mass: Num, radius: Num, height: Num):
        radius_height = 3.0 * (radius ** 2.0) + height ** 2.0

        return Inertia(
                mass * np_.eye(3),
                1.0 / 12.0 * mass * np_.diag((
                        radius_height,
                        radius_height,
                        6.0 * (radius ** 2.0)
                ))
        )

    @staticmethod
    def sphere(mass: Num, radius: Num):
        radius_squared = radius ** 2.0

        return Inertia(
                mass * np_.eye(3),
                2.0 / 3.0 * mass * np_.diag((
                        radius_squared,
                        radius_squared,
                        radius_squared
                ))
        )

    @staticmethod
    def tube(mass: Num, inner_radius: Num, outer_radius: Num, height: Num):
        radius = (inner_radius ** 2.0) + (outer_radius ** 2.0)
        rh = 3.0 * (radius ** 2.0) + height ** 2.0

        return Inertia(
                mass * np_.eye(3),
                1.0 / 12.0 * mass * np_.diag((
                        rh,
                        rh,
                        6.0 * (radius ** 2.0)
                ))
        )

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, inertia: Matrix):
        self._linear = np_.asarray(inertia)

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, inertia: Matrix):
        self._angular = np_.asarray(inertia)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.linear, other.linear) \
               and np_.allclose(self.angular, other.angular)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((id(self.angular), id(self.linear)))

    __repr__ = make_repr(
            'linear',
            'angular'
    )


__all__ = [
        'Inertia',
]
