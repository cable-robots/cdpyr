from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Linear(BaseObject):
    _position: np_.ndarray = np_.asarray((0., 0., 0.))
    _velocity: np_.ndarray = np_.asarray((0., 0., 0.))
    _acceleration: np_.ndarray = np_.asarray((0., 0., 0.))

    def __init__(self,
                 position: Optional[Vector] = None,
                 velocity: Optional[Vector] = None,
                 acceleration: Optional[Vector] = None
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

        _validator.linalg.space_coordinate(position, 'position')

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

        _validator.linalg.space_coordinate(velocity, 'velocity')

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

        _validator.linalg.space_coordinate(acceleration, 'acceleration')

        self._acceleration = acceleration

    @acceleration.deleter
    def acceleration(self):
        del self._acceleration

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.position, other.position) \
               and np_.allclose(self.velocity, other.velocity) \
               and np_.allclose(self.acceleration, other.acceleration)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.position < other.position).any() \
               or (self.velocity < other.velocity).any() \
               or (self.acceleration < other.acceleration).any()

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.position <= other.position).any() \
               or (self.velocity <= other.velocity).any() \
               or (self.acceleration <= other.acceleration).any()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.position > other.position).any() \
               or (self.velocity > other.velocity).any() \
               or (self.acceleration > other.acceleration).any()

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.position >= other.position).any() \
               or (self.velocity >= other.velocity).any() \
               or (self.acceleration >= other.acceleration).any()

    def __hash__(self):
        return hash((id(self.acceleration),
                     id(self.position),
                     id(self.velocity)))

    __repr__ = make_repr(
        'position',
        'velocity',
        'acceleration'
    )


__all__ = [
    'Linear',
]
