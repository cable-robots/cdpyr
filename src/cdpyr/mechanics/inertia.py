from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix

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

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, inertia: Matrix):
        inertia = np_.asarray(inertia)

        _validator.linalg.dimensions(inertia, 2, 'linear')
        _validator.linalg.shape(inertia, (3, 3), 'linear')
        _validator.numeric.positive(np_.diag(inertia), 'linear')

        self._linear = inertia

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, inertia: Matrix):
        inertia = np_.asarray(inertia)

        _validator.linalg.dimensions(inertia, 2, 'angular')
        _validator.linalg.shape(inertia, (3, 3), 'angular')
        _validator.numeric.nonnegative(inertia.diagonal(), 'angular')

        self._angular = inertia

    __repr__ = make_repr(
        'linear',
        'angular'
    )


__all__ = [
    'Inertia',
]
