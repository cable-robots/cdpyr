import numpy as np_
from magic_repr import make_repr

from cdpyr.typedef import Vector


class Linear(object):
    _position: np_.ndarray
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

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

        if position.ndim != 1:
            raise ValueError(
                'invalid dimension. position must be a 1-dimensional list or '
                'array')

        # if position is not of shape (3,) we will pad it with zeros at the end
        if position.shape[0] != 3:
            position = np_.pad(position, (0, 3 - position.shape[0]))

        if position.shape != (3,):
            raise ValueError(
                'invalid shape. position must be a 3-element list or a (3,'
                ') numpy array')

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

        if velocity.ndim != 1:
            raise ValueError(
                'invalid dimension. velocity must be a 1-dimensional list or '
                'array')

        if velocity.shape[0] != 3:
            velocity = np_.pad(velocity, (0, 3 - velocity.shape[0]))

        if velocity.shape != (3,):
            raise ValueError(
                'invalid shape. velocity must be a 3-element list or a (3,'
                ') numpy array')

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

        if acceleration.ndim != 1:
            raise ValueError(
                'invalid dimension. acceleration must be a 1-dimensional list '
                'or array')

        if acceleration.shape[0] != 3:
            acceleration = np_.pad(acceleration, (0, 3 - acceleration.shape[0]))

        if acceleration.shape != (3,):
            raise ValueError(
                'invalid shape. acceleration must be a 3-element list or a (3,'
                ') numpy array')

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
