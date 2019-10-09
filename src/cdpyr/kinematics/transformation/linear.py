import numpy as np_
from magic_repr import make_repr

from cdpyr.typing import Vector

from cdpyr import  validator as _validator


class Linear(object):
    _position: np_.ndarray = np_.asarray((0., 0., 0.))
    _velocity: np_.ndarray = np_.asarray((0., 0., 0.))
    _acceleration: np_.ndarray = np_.asarray((0., 0., 0.))

    def __init__(self,
                 position: Vector = None,
                 velocity: Vector = None,
                 acceleration: Vector = None
                 ):
        self.position = position \
            if position is not None \
            else [0.0, 0.0, 0.0]
        self.velocity = velocity \
            if velocity is not None \
            else [0.0, 0.0, 0.0]
        self.acceleration = acceleration \
            if acceleration is not None \
            else [0.0, 0.0, 0.0]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector):
        position = np_.asarray(position)

        _validator.dimensions(position, 1, 'position')
        _validator.shape(position, (3, ), 'position')

        self._position = position

    @position.deleter
    def position(self):
        del self._position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Vector):
        velocity = np_.asarray(velocity)

        _validator.dimensions(velocity, 1, 'velocity')
        _validator.shape(velocity, (3, ), 'velocity')

        self._velocity = velocity

    @velocity.deleter
    def velocity(self):
        del self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Vector):
        acceleration = np_.asarray(acceleration)

        _validator.dimensions(acceleration, 1, 'acceleration')
        _validator.shape(acceleration, (3, ), 'acceleration')

        self._acceleration = acceleration

    @acceleration.deleter
    def acceleration(self):
        del self._acceleration


Linear.__repr__ = make_repr(
    'position',
    'velocity',
    'acceleration'
)

__all__ = [
    'Linear',
]
