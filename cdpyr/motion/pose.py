from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mechanics.transformation.angular import Angular as \
    AngularTransformation
from cdpyr.mechanics.transformation.linear import Linear as LinearTransformation
from cdpyr.mixins.lists import DispatcherList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Pose(object):
    _linear: LinearTransformation
    _angular: AngularTransformation
    _time: _TNum

    def __init__(self,
                 position: Optional[Tuple[_TVector, _TMatrix]] = None,
                 velocity: Optional[Tuple[_TVector, _TVector]] = None,
                 acceleration: Optional[Tuple[_TVector, _TVector]] = None,
                 time: _TNum = None,
                 ):
        self.linear = LinearTransformation()
        self.angular = AngularTransformation()

        self.position = position or (
            [0.0, 0.0, 0.0],
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        self.velocity = velocity or ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        self.acceleration = acceleration or ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        self.time = time or 0

    @property
    def state(self):
        return self._linear

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time: _TNum):
        self._time = time

    @time.deleter
    def time(self):
        del self._time

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

    def __lt__(self, other: object):
        try:
            return self.time < other.time
        except AttributeError:
            return self < other

    def __le__(self, other: object):
        try:
            return self.time <= other.time
        except AttributeError:
            return self < other

    def __gt__(self, other: object):
        try:
            return self.time > other.time
        except AttributeError:
            return self < other

    def __ge__(self, other: object):
        try:
            return self.time >= other.time
        except AttributeError:
            return self < other


Pose.__repr__ = make_repr(
    'time',
    'position',
    'velocity',
    'acceleration'
)


class PoseList(DispatcherList):
    pass


__all__ = ['Pose', 'PoseList']
