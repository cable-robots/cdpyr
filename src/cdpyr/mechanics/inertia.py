from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.typing import Matrix, Num, Vector

from cdpyr import  validator as _validator


class Inertia(object):
    _linear: np_.ndarray
    _angular: np_.ndarray

    def __init__(self,
                 linear: Union[Vector, Num] = None,
                 angular: Union[Vector, Matrix] = None
                 ):
        self.linear = linear if linear else np_.zeros(3)
        self.angular = angular if angular else np_.zeros((3, 3))

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, inertia: Union[Vector, Num]):
        self._linear = np_.asarray(inertia)

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, inertia: Union[Matrix, Vector]):
        self._angular = np_.asarray(inertia)


Inertia.__repr__ = make_repr(
    'linear',
    'angular'
)

__all__ = [
    'Inertia',
]
