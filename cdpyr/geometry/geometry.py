from abc import ABC
from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Geometry(ABC):
    _mass: float

    def moment_of_inertia(self):
        raise NotImplementedError('method not implemented by child class.')

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: _TNum):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        self._mass = mass

    @mass.deleter
    def mass(self):
        del self._mass


Geometry.__repr__ = make_repr()

__all__ = ['Geometry']
