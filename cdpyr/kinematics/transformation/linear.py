from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.typedefs import Num, Vector, Matrix


class Linear(object):
    _position: np_.ndarray
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

    def __init__(self,
                 position: Vector = None,
                 velocity: Vector = None,
                 acceleration: Vector = None
                 ):
        self.position = position or [0.0, 0.0, 0.0]
        self.velocity = velocity or [0.0, 0.0, 0.0]
        self.acceleration = acceleration or [0.0, 0.0, 0.0]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Union[Vector, np_.ndarray]):
        position = np_.asarray(position)

        if position.ndim != 1:
            raise ValueError(
                'invalid dimension. position must be a 1-dimensional list or '
                'array')

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
    def velocity(self, velocity: Union[Vector, np_.ndarray]):
        velocity = np_.asarray(velocity)

        if velocity.ndim != 1:
            raise ValueError(
                'invalid dimension. velocity must be a 1-dimensional list or '
                'array')

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
    def acceleration(self, acceleration: Union[Vector, np_.ndarray]):
        acceleration = np_.asarray(acceleration)

        if acceleration.ndim != 1:
            raise ValueError(
                'invalid dimension. acceleration must be a 1-dimensional list '
                'or array')

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


class LinearSchema(Schema):
    position = fields.List(fields.Float())
    velocity = fields.List(fields.Float())
    acceleration = fields.List(fields.Float())

    __model__ = Linear

    @post_load
    def make_linear(self, data):
        return self.__model__(**data)


__all__ = [
    'Linear',
    'LinearSchema',
]
