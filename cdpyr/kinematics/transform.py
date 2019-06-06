from typing import Iterable
from typing import List
from typing import Union

import numpy as np_
from scipy.spatial.transform import Rotation as Rotation_


class Linear(object):
    """
    Internal position storage variable
    """
    _linpos: np_.ndarray
    _linvel: np_.ndarray
    _linacc: np_.ndarray

    def __init__(self,
                 position: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 velocity: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 acceleration: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 *args,
                 **kwargs):
        self.linear_position = position if position is not None else np_.zeros(3)
        self.linear_velocity = velocity if velocity is not None else np_.zeros(3)
        self.linear_acceleration = acceleration if acceleration is not None else np_.zeros(
            3)

    @property
    def linear_acceleration(self) -> np_.ndarray:
        return self._linacc

    @linear_acceleration.setter
    def linear_acceleration(self, a: Union[np_.ndarray, list, Iterable, int, float]):
        a = np_.asarray(a, dtype=np_.float64)

        if not a.shape == (3,):
            raise ValueError('linear_acceleration must be of shape (3, )')

        self._linacc = a

    @property
    def linear_position(self) -> np_.ndarray:
        return self._linpos

    @linear_position.setter
    def linear_position(self, p: Union[np_.ndarray, list, Iterable, int, float]):
        p = np_.asarray(p, dtype=np_.float64)

        if not p.shape == (3,):
            raise ValueError('linear_position must be of shape (3, )')

        self._linpos = p

    @property
    def linear_velocity(self) -> np_.ndarray:
        return self._linvel

    @linear_velocity.setter
    def linear_velocity(self, v: Union[np_.ndarray, list, Iterable, int, float]):
        v = np_.asarray(v, dtype=np_.float64)

        if not v.shape == (3,):
            raise ValueError('linear_velocity must be of shape (3, )')

        self._linvel = v


class Angular(object):
    _angpos: Rotation_
    _angvel: np_.ndarray
    _angacc: np_.ndarray

    def __init__(self,
                 orientation: Rotation_ = None,
                 quaternion: Union[list, np_.ndarray, Iterable, int, float] =
                 None,
                 dcm: Union[List[list], np_.ndarray, Iterable, int, float] =
                 None,
                 rotvec: Union[list, np_.ndarray, Iterable, int, float] = None,
                 euler: Union[list, np_.ndarray, Iterable, int, float] = None,
                 velocity: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 acceleration: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 *args,
                 **kwargs):

        self.orientation = Rotation_.from_euler('ZYX', [0, 0, 0])
        if orientation is not None:
            self.orientation = orientation
        elif quaternion is not None:
            self.quaternion = quaternion
        elif dcm is not None:
            self.dcm = dcm
        elif rotvec is not None:
            self.rotvec = rotvec
        elif euler is not None:
            self.euler = euler
        self.angular_velocity = velocity if velocity is not None else np_.zeros(3)
        self.angular_acceleration = acceleration if acceleration is not None else np_.zeros(
            3)

    @property
    def angular_acceleration(self) -> np_.ndarray:
        return self._angacc

    @angular_acceleration.setter
    def angular_acceleration(self, a: Union[np_.ndarray, list, Iterable, int, float]):
        a = np_.asarray(a, dtype=np_.float64)

        if not a.shape == (3,):
            raise ValueError('angular_acceleration must be of shape (3, )')

        self._angacc = a

    @property
    def angular_velocity(self) -> np_.ndarray:
        return self._angvel

    @angular_velocity.setter
    def angular_velocity(self, v: Union[np_.ndarray, list, Iterable, int, float]):
        v = np_.asarray(v, dtype=np_.float64)

        if not v.shape == (3,):
            raise ValueError('angular_velocity must be of shape (3, )')

        self._angvel = v

    @property
    def dcm(self) -> np_.ndarray:
        return self.orientation.as_dcm()

    @dcm.setter
    def dcm(self, r: Union[List[list], np_.ndarray, Iterable, int, float]):
        self.orientation = Rotation_.from_dcm(r)

    @property
    def euler(self) -> np_.ndarray:
        return self.orientation.as_euler('ZYX')

    @euler.setter
    def euler(self, euler: Union[list, np_.ndarray, Iterable]):
        self.orientation = Rotation_.from_euler('ZYX', euler)

    @property
    def orientation(self):
        return self._angpos

    @orientation.setter
    def orientation(self, orientation: Rotation_):
        if not isinstance(orientation, Rotation_):
            raise ValueError('orientation must be of type '
                             'scipy.spatial.transform.Rotation')

        self._angpos = orientation

    @property
    def quaternion(self) -> np_.ndarray:
        return self.orientation.as_quat()

    @quaternion.setter
    def quaternion(self, q: Union[list, np_.ndarray, Iterable, int, float]):
        self.orientation = Rotation_.from_quat(q)

    @property
    def rotvec(self) -> np_.ndarray:
        return self.orientation.as_rotvec()

    @rotvec.setter
    def rotvec(self, rotvec: Union[np_.ndarray, Iterable, int, float]):
        self.orientation.from_rotvec(rotvec)
