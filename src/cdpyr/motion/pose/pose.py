from typing import Optional, Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    homogenous as _homogenous,
    linear as _linear,
)
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pose(BaseObject):
    _linear: '_linear.Linear'
    _angular: '_angular.Angular'
    _time: Num

    def __init__(self,
                 position: Optional[Tuple[Vector, Matrix]] = None,
                 velocity: Optional[Tuple[Vector, Vector]] = None,
                 acceleration: Optional[Tuple[Vector, Vector]] = None,
                 linear: Optional['_linear.Linear'] = None,
                 angular: Optional['_angular.Angular'] = None,
                 time: Optional[Num] = np_.NaN,
                 ):
        if linear is None:
            self.linear = _linear.Linear(
                position[0]
                if isinstance(position, Sequence)
                   and 0 < len(position)
                   and position is not None
                else np_.zeros((3,)),
                velocity[0]
                if isinstance(velocity, Sequence)
                   and 0 < len(velocity)
                   and velocity is not None
                else np_.zeros((3,)),
                acceleration[0]
                if isinstance(acceleration, Sequence)
                   and 0 < len(acceleration)
                   and acceleration is not None
                else np_.zeros((3,)),
            )
        else:
            self.linear = linear

        if angular is None:
            self.angular = _angular.Angular(
                dcm=position[1]
                if isinstance(position, Sequence)
                   and 1 < len(position)
                   and position[1] is not None
                else np_.eye(3),
                angular_velocity=velocity[1]
                if isinstance(velocity, Sequence)
                   and 1 < len(velocity)
                   and velocity is not None
                else np_.zeros((3,)),
                angular_acceleration=acceleration[1]
                if isinstance(acceleration, Sequence)
                   and 1 < len(acceleration)
                   and acceleration is not None
                else np_.zeros((3,)),
            )
        else:
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
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, linear: '_linear.Linear'):
        self._linear = linear

    @linear.deleter
    def linear(self):
        del self._linear

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: '_angular.Angular'):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self._angular

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

    def __eq__(self, other: Union['Pose', object]):
        try:
            return np_.allclose(self.state, other.state) \
                   and np_.allclose(self.time, other.time, equal_nan=True)
        except AttributeError as AttributeE:
            try:
                return np_.allclose(self.state, np_.asarray(other))
            except ValueError as ValueE:
                return np_.allclose(np_.hstack((self.time, self.state)),
                                    np_.asarray(other), equal_nan=True)
            except TypeError as TypeE:
                raise TypeError from None

    def __ne__(self, other: Union['Pose', object]):
        # if times differ => different poses
        # if times are equal and states differ => different poses
        try:
            return not (np_.allclose(self.state, other.state)
                        and np_.allclose(self.time, other.time, equal_nan=True))
        except AttributeError as AttributeE:
            try:
                return not np_.allclose(self.state, np_.asarray(other))
            except ValueError as ValueE:
                return not np_.allclose(np_.hstack((self.time, self.state)),
                                        np_.asarray(other), equal_nan=True)
            except TypeError as TypeE:
                raise TypeError from None

    def __lt__(self, other: Union['Pose', object]):
        try:
            return self.time < other.time
        except AttributeError as AttributeE:
            try:
                return self.time < other
            except TypeError as TypeE:
                raise TypeError from None

    def __le__(self, other: Union['Pose', object]):
        try:
            return self.time <= other.time
        except AttributeError as AttributeE:
            try:
                return self.time <= other
            except TypeError as TypeE:
                raise TypeError from None

    def __gt__(self, other: Union['Pose', object]):
        try:
            return self.time > other.time
        except AttributeError as AttributeE:
            try:
                return self.time > other
            except TypeError as TypeE:
                raise TypeError from None

    def __ge__(self, other: Union['Pose', object]):
        try:
            return self.time >= other.time
        except AttributeError as AttributeE:
            try:
                return self.time >= other
            except TypeError as TypeE:
                raise TypeError from None

    __repr__ = make_repr(
        'time',
        'position',
        'velocity',
        'acceleration'
    )


__all__ = [
    'Pose',
]
