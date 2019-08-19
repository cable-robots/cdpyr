from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Linear(object):
    _position: np_.ndarray
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

    def __init__(self,
                 position: _TVector = None,
                 velocity: _TVector = None,
                 acceleration: _TVector = None
                 ):
        self.position = position or [0.0, 0.0, 0.0]
        self.velocity = velocity or [0.0, 0.0, 0.0]
        self.acceleration = acceleration or [0.0, 0.0, 0.0]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Union[_TVector, np_.ndarray]):
        self._position = np_.asarray(position)

    @position.deleter
    def position(self):
        del self._position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Union[_TVector, np_.ndarray]):
        self._velocity = np_.asarray(velocity)

    @velocity.deleter
    def velocity(self):
        del self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Union[_TVector, np_.ndarray]):
        self._acceleration = np_.asarray(acceleration)

    @acceleration.deleter
    def acceleration(self):
        del self._acceleration


Linear.__repr__ = make_repr(
    'position',
    'velocity',
    'acceleration'
)

__all__ = ['Linear']
