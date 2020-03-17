from __future__ import annotations

from collections import UserList
from typing import Optional, Tuple, Union, Sequence

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    homogenous as _homogenous,
    linear as _linear
)
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pose(BaseObject):
    linear: _linear.Linear
    angular: _angular.Angular
    _time: Num

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 velocity: Optional[Vector] = None,
                 angular_velocity: Optional[Vector] = None,
                 acceleration: Optional[Vector] = None,
                 angular_acceleration: Optional[Vector] = None,
                 time: Optional[Num] = np_.NaN,
                 linear: Optional[_linear.Linear] = None,
                 angular: Optional[_angular.Angular] = None,
                 **kwargs):
        super().__init__(**kwargs)
        # no linear object given, then build it from the arguments and their
        # defaults
        if linear is None:
            linear = _linear.Linear(
                    position,
                    velocity,
                    acceleration
            )
        # no angular object given, then build it from the arguments and their
        # defaults
        if angular is None:
            angular = _angular.Angular(
                    dcm,
                    angular_velocity,
                    angular_acceleration
            )

        # assign processed properties
        self.linear = linear
        self.angular = angular
        self.time = time

    @property
    def state(self):
        return np_.hstack((self.linear.position, self.angular.quaternion))

    @property
    def transformation(self):
        return _homogenous.Homogenous(
                self.linear.position,
                self.angular.dcm
        )

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time: Num):
        self._time = time if time is not None else np_.NaN

    @time.deleter
    def time(self):
        del self._time

    @property
    def position(self):
        return [self.linear.position, self.angular.dcm]

    @position.setter
    def position(self, position: Tuple[Vector, Matrix]):
        self.linear.position = position[0]
        self.angular.dcm = position[1]

    @position.deleter
    def position(self):
        del self.linear.position
        del self.angular.dcm

    @property
    def velocity(self):
        return [self.linear.velocity, self.angular.angular_velocity]

    @velocity.setter
    def velocity(self, velocity: Tuple[Vector, Vector]):
        self.linear.velocity = velocity[0]
        self.angular.velocity = velocity[1]

    @velocity.deleter
    def velocity(self):
        del self.linear.velocity
        del self.angular.angular_velocity

    @property
    def acceleration(self):
        return [self.linear.acceleration, self.angular.angular_acceleration]

    @acceleration.setter
    def acceleration(self, acceleration: Tuple[Vector, Vector]):
        self.linear.acceleration = acceleration[0]
        self.angular.angular_acceleration = acceleration[1]

    @acceleration.deleter
    def acceleration(self):
        del self.linear.acceleration
        del self.angular.angular_acceleration

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.time, other.time, equal_nan=True) \
               and self.linear == other.linear \
               and self.angular == other.angular

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.angular, self.linear, self.time))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return self.time < other.time \
               or self.linear < other.linear \
               or self.angular < other.angular

    def __le__(self, other: Union['Pose', object]):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.time <= other.time \
               or self.linear <= other.linear \
               or self.angular <= other.angular

    def __gt__(self, other: Union['Pose', object]):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return self.time > other.time \
               or self.linear > other.linear \
               or self.angular > other.angular

    def __ge__(self, other: Union['Pose', object]):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.time >= other.time \
               or self.linear >= other.linear \
               or self.angular >= other.angular

    __repr__ = make_repr(
            'time',
            'position',
            'velocity',
            'acceleration'
    )


class PoseList(UserList, BaseObject):
    data: Sequence[Pose]

    @property
    def acceleration(self):
        return (pose.acceleration for pose in self.data)

    @property
    def angular(self):
        return (pose.angular for pose in self.data)

    @property
    def linear(self):
        return (pose.linear for pose in self.data)

    @property
    def position(self):
        return (pose.position for pose in self.data)

    @property
    def state(self):
        return (pose.state for pose in self.data)

    @property
    def time(self):
        return (pose.time for pose in self.data)

    @property
    def transformation(self):
        return (pose.transformation for pose in self.data)

    @property
    def velocity(self):
        return (pose.velocity for pose in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.data))

    __repr__ = make_repr(
            'data'
    )


ZeroPose = Pose([0.0, 0.0, 0.0],
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

__all__ = [
        'Pose',
        'PoseList',
        'ZeroPose',
]
