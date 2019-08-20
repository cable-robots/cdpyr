from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load
from scipy.spatial.transform import Rotation

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Angular(object):
    _angular_rotation: Rotation = Rotation.from_quat([0.0, 0.0, 0.0, 1.0])
    _angular_velocity: np_.ndarray = np_.array([0.0, 0.0, 0.0])
    _angular_acceleration: np_.ndarray = np_.array([0.0, 0.0, 0.0])
    _rotation_sequence: str = 'zyx'

    def __init__(self,
                 angular_position: _TVector = None,
                 angular_velocity: _TVector = None,
                 angular_acceleration: _TVector = None,
                 rotation_sequence: str = None
                 ):
        """ A kinematic angular transformation object.

        This object represents a kinematic transformation on the orientation
        or angular space. It allows for describing and reading the angular
        orientation in different ways like DCM (orientation matrix),
        quaternion, rotation vectors, or Euler angles.

        :param _TVector|list angular_position: Optional angular position
        given as Euler angles, defined in the `rotation_sequence` parameter
        :param _TVector|list angular_velocity: Optional angular velocity
        about the three principal axes of rotation.
        :param _TVector|list angular_acceleration: Optional angular
        acceleration about the three principal axes of rotation.
        :param str rotation_sequence: Optional rotation sequence that should
        internally be used when converting to Euler angles.
        """
        self.sequence = rotation_sequence or 'zyx'
        self.angular_position = angular_position or [0.0, 0.0, 0.0]
        self.angular_velocity = angular_velocity or [0.0, 0.0, 0.0]
        self.angular_acceleration = angular_acceleration or [0.0, 0.0, 0.0]

    @property
    def rotation(self):
        return self._angular_rotation

    @rotation.setter
    def rotation(self, rotation: Rotation):
        self._angular_rotation = rotation

    @rotation.deleter
    def rotation(self):
        del self._angular_rotation

    @property
    def sequence(self):
        return self._rotation_sequence

    @sequence.setter
    def sequence(self, sequence: str):
        self._rotation_sequence = sequence

    @sequence.deleter
    def sequence(self):
        del self._rotation_sequence

    @property
    def angular_position(self):
        return self.euler

    @angular_position.setter
    def angular_position(self, position: _TVector):
        self.euler = position

    @angular_position.deleter
    def angular_position(self):
        del self.euler

    @property
    def euler(self):
        return self._angular_rotation.as_euler(self.sequence)

    @euler.setter
    def euler(self, euler: _TVector):
        self.rotation = Rotation.from_euler(self.sequence, euler)

    @euler.deleter
    def euler(self):
        del self.rotation

    @property
    def dcm(self):
        return self._angular_rotation.as_dcm()

    @dcm.setter
    def dcm(self, dcm: _TMatrix):
        self.rotation = Rotation.from_dcm(dcm)

    @dcm.deleter
    def dcm(self):
        del self.rotation

    @property
    def quaternion(self):
        return self._angular_rotation.as_quat()

    @quaternion.setter
    def quaternion(self, quaternion: _TVector):
        self.rotation = Rotation.from_quat(quaternion)

    @quaternion.deleter
    def quaternion(self):
        del self.rotation

    @property
    def rotvec(self):
        return self._angular_rotation.as_rotvec()

    @rotvec.setter
    def rotvec(self, rotvec: _TVector):
        self.rotation = Rotation.from_rotvec(rotvec)

    @rotvec.deleter
    def rotvec(self):
        del self.rotation

    @property
    def angular_velocity(self):
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, velocity: _TVector):
        velocity = np_.asarray(velocity)

        if velocity.ndim != 1:
            raise ValueError(
                'invalid dimension. angular_velocity must be a 1-dimensional '
                'list or array')

        if velocity.shape != (3,):
            raise ValueError(
                'invalid shape. angular_velocity must be a 3-element list or '
                'a (3,) numpy array')

        self._angular_velocity = velocity

    @angular_velocity.deleter
    def angular_velocity(self):
        del self._angular_velocity

    @property
    def angular_acceleration(self):
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, acceleration: _TVector):
        acceleration = np_.asarray(acceleration)

        if acceleration.ndim != 1:
            raise ValueError(
                'invalid dimension. angular_acceleration must be a '
                '1-dimensional list or array')

        if acceleration.shape != (3,):
            raise ValueError(
                'invalid shape. angular_acceleration must be a 3-element list '
                'or a (3,) numpy array')

        self._angular_acceleration = acceleration

    @angular_acceleration.deleter
    def angular_acceleration(self):
        del self._angular_acceleration


Angular.__repr__ = make_repr(
    'dcm',
    'angular_velocity',
    'angular_acceleration'
)


class AngularSchema(Schema):
    dcm = fields.List(fields.List(fields.Float()))
    angular_velocity = fields.List(fields.Float())
    angular_acceleration = fields.List(fields.Float())

    __model__ = Angular

    @post_load
    def make_angular(self, data):
        return self.__model__(**data)


__all__ = ['Angular', 'AngularSchema']
