from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

import numpy as np_
from scipy.spatial.transform import Rotation as Rotation_


class Linear(object):
    """
    Internal position storage variable
    """
    _position: np_.ndarray
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

    def __init__(self,
                 position: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 velocity: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 acceleration: Union[np_.ndarray, list, Iterable, int, float] =
                 None):
        self.position = position if position is not None else np_.zeros(3)
        self.velocity = velocity if velocity is not None else np_.zeros(3)
        self.acceleration = acceleration if acceleration is not None else np_.zeros(
            3)

    @property
    def acceleration(self) -> np_.ndarray:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, a: Union[np_.ndarray, list, Iterable, int, float]):
        if not isinstance(a, np_.ndarray):
            a = np_.array(a, dtype=np_.float64)

        if not a.shape == (3,):
            raise ValueError('acceleration must be of shape (3, )')

        self._acceleration = a

    @property
    def position(self) -> np_.ndarray:
        return self._position

    @position.setter
    def position(self, p: Union[np_.ndarray, list, Iterable, int, float]):
        if not isinstance(p, np_.ndarray):
            p = np_.array(p, dtype=np_.float64)

        if not p.shape == (3,):
            raise ValueError('position must be of shape (3, )')

        self._position = p

    @property
    def velocity(self) -> np_.ndarray:
        return self._velocity

    @velocity.setter
    def velocity(self, v: Union[np_.ndarray, list, Iterable, int, float]):
        if not isinstance(v, np_.ndarray):
            v = np_.array(v, dtype=np_.float64)

        if not v.shape == (3,):
            raise ValueError('velocity must be of shape (3, )')

        self._velocity = v


class Angular(object):
    _position: Rotation_
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

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
                 None):

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
        self.velocity = velocity if velocity is not None else np_.zeros(3)
        self.acceleration = acceleration if acceleration is not None else np_.zeros(
            3)

    @property
    def acceleration(self) -> np_.ndarray:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, a: Union[np_.ndarray, list, Iterable, int, float]):
        if not isinstance(a, np_.ndarray):
            a = np_.array(a, dtype=np_.float64)

        if not a.shape == (3,):
            raise ValueError('acceleration must be of shape (3, )')

        self._acceleration = a

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
        return self._position

    @orientation.setter
    def orientation(self, orientation: Rotation_):
        if not isinstance(orientation, Rotation_):
            raise ValueError('orientation must be of type '
                             'scipy.spatial.transform.Rotation')

        self._position = orientation

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

    @property
    def velocity(self) -> np_.ndarray:
        return self._velocity

    @velocity.setter
    def velocity(self, v: Union[np_.ndarray, list, Iterable, int, float]):
        if not isinstance(v, np_.ndarray):
            v = np_.array(v, dtype=np_.float64)

        if not v.shape == (3,):
            raise ValueError('velocity must be of shape (3, )')

        self._velocity = v
