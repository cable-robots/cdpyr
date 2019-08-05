from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np_
from magic_repr import make_repr

from ..mechanics.transformation import Angular as AngularTransformation
from ..mechanics.transformation import Linear as LinearTransformation

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Pose(object):
    _linear: LinearTransformation
    _angular: AngularTransformation

    def __init__(self,
                 position: Optional[Tuple[_TVector, _TMatrix]] = None,
                 velocity: Optional[Tuple[_TVector, _TVector]] = None,
                 acceleration: Optional[Tuple[_TVector, _TVector]] = None
                 ):
        self.linear = LinearTransformation()
        self.angular = AngularTransformation()

        self.position = position if position is not None else (
            [0.0, 0.0, 0.0], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        self.velocity = velocity if velocity is not None else (
            [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        self.acceleration = acceleration if acceleration is not None else (
            [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])

    @property
    def state(self):
        return self._linear

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, linear: LinearTransformation):
        self._linear = linear

    @linear.deleter
    def linear(self):
        del self._linear

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: AngularTransformation):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self._angular

    @property
    def position(self):
        return self.linear.position, self.angular.dcm

    @position.setter
    def position(self, position: Tuple[_TVector, _TMatrix]):
        self.linear.position = position[0]
        self.angular.dcm = position[1]

    @position.deleter
    def position(self):
        del self.linear.position
        del self.angular.rotation

    @property
    def velocity(self):
        return self.linear.velocity, self.angular.angular_velocity

    @velocity.setter
    def velocity(self, velocity: Tuple[_TVector, _TVector]):
        self.linear.velocity = velocity[0]
        self.angular.velocity = velocity[1]

    @velocity.deleter
    def velocity(self):
        del self.linear.velocity
        del self.angular.angular_velocity

    @property
    def acceleration(self):
        return self.linear.acceleration, self.angular.angular_acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Tuple[_TVector, _TVector]):
        self.linear.acceleration = acceleration[0]
        self.angular.angular_acceleration = acceleration[1]

    @acceleration.deleter
    def acceleration(self):
        del self.linear.acceleration
        del self.angular.angular_acceleration


Pose.__repr__ = make_repr('position', 'velocity', 'acceleration')

__all__ = ['Pose']
