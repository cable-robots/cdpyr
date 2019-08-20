from typing import Optional, Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.kinematics.transformation.angular import Angular as \
    AngularTransformation
from cdpyr.kinematics.transformation.homogenous import Homogenous
from cdpyr.kinematics.transformation.linear import Linear as \
    LinearTransformation
from cdpyr.mixins.lists import DispatcherList

from cdpyr.typedefs import Num, Vector, Matrix


class Pose(object):
    _linear: LinearTransformation
    _angular: AngularTransformation
    _time: Num

    def __init__(self,
                 position: Optional[Tuple[Vector, Matrix]] = None,
                 velocity: Optional[Tuple[Vector, Vector]] = None,
                 acceleration: Optional[Tuple[Vector, Vector]] = None,
                 time: Num = None,
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
        return np_.hstack([self.linear.position, self.angular.quaternion])

    @property
    def transformationmatrix(self):
        return Homogenous(translation=self.linear.position,
                          rotation=self.angular.dcm)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time: Num):
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
    def position(self, position: Tuple[Vector, Matrix]):
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
    def velocity(self, velocity: Tuple[Vector, Vector]):
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
    def acceleration(self, acceleration: Tuple[Vector, Vector]):
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


class PoseSchema(Schema):
    time = fields.Float()
    position = fields.List(fields.List(fields.Float()))
    velocity = fields.List(fields.List(fields.Float()))
    acceleration = fields.List(fields.List(fields.Float()))

    __model__ = Pose

    @post_load
    def make_pose(self, data):
        return self.__model__(**data)


class PoseList(DispatcherList):
    pass


__all__ = ['Pose', 'PoseList', 'PoseSchema']
