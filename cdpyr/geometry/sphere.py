from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.geometry.geometry import Geometry

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Sphere(Geometry):
    _diameter: float

    def __init__(self,
                 diameter: Optional[_TNum] = None,
                 ):
        self.diameter = diameter or 0

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: _TNum):
        if diameter < 0:
            raise ValueError('diameter must be nonnegative')

        self._diameter = diameter

    @diameter.deleter
    def diameter(self):
        del self._diameter

    @property
    def radius(self):
        return self._diameter / 2.0

    @radius.setter
    def radius(self, radius: _TNum):
        if radius < 0:
            raise ValueError('radius must be nonnegative')

        self.diameter = 2.0 * radius

    @radius.deleter
    def radius(self):
        del self.diameter

    def moment_of_inertia(self):
        mass = self.mass
        rs = self.radius ** 2.0

        return 2.0 / 3.0 * mass * np_.array((
            rs,
            rs,
            rs
        ))


Sphere.__repr__ = make_repr(
    'diameter'
)


class SphereSchema(Schema):
    diameter = fields.Float()

    __model__ = Sphere

    @post_load
    def make_user(self, data):
        return self.__model__(**data)


__all__ = ['Sphere', 'SphereSchema']
