from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Inertia(object):
    _linear: np_.ndarray
    _angular: np_.ndarray

    def __init__(self,
                 linear: Union[_TVector, _TNum] = None,
                 angular: Union[_TVector, _TMatrix] = None
                 ):
        self.linear = linear if linear else np_.zeros(3)
        self.angular = angular if angular else np_.zeros((3, 3))

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, inertia: Union[_TVector, _TNum]):
        self._linear = np_.asarray(inertia)

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, inertia: Union[_TMatrix, _TVector]):
        self._angular = np_.asarray(inertia)


Inertia.__repr__ = make_repr(
    'linear',
    'angular'
)

__all__ = ['Inertia']
