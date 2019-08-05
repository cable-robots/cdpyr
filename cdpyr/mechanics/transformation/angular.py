from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr
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
        self.sequence = rotation_sequence if rotation_sequence is not None \
            else 'zyx'
        self.angular_position = angular_position if angular_position is not \
                                                    None else [0.0, 0.0, 0.0]
        self.angular_velocity = angular_velocity if angular_velocity is not \
                                                    None else [0.0, 0.0, 0.0]
        self.angular_acceleration = angular_acceleration if \
            angular_acceleration is not None else [0.0, 0.0, 0.0]

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
        self._angular_velocity = np_.asarray(velocity)

    @angular_velocity.deleter
    def angular_velocity(self):
        del self._angular_velocity

    @property
    def angular_acceleration(self):
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, acceleration: _TVector):
        self._angular_acceleration = np_.asarray(acceleration)

    @angular_acceleration.deleter
    def angular_acceleration(self):
        del self._angular_acceleration


Angular.__repr__ = make_repr('dcm', 'angular_velocity', 'angular_acceleration')

__all__ = ['Angular']
