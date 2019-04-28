from typing import Union
from typing import List

import numpy as np_
import quaternion as np_quaternion


class Orientable(object):

    def __init__(self, orientation: Union[np_.quaternion, np_.ndarray, list,
                                          List[list]] = None):
        if orientation is not None:
            # list[list]: rotation matrix
            # list: quaternion
            if orientation is list:
                try:
                    self.rotation_matrix = orientation
                except Exception as e:
                    self.quaternion = orientation
            # numpy.ndarray: rotation matrix
            # numpy.ndarray: quaternion
            elif isinstance(orientation, np_.ndarray):
                try:
                    self.rotation_matrix = orientation
                except Exception as e:
                    self.quaternion = orientation
        else:
            self.quaternion = np_quaternion.one

    @property
    def rotation_matrix(self):
        return np_quaternion.as_rotation_matrix(self.quaternion)

    @rotation_matrix.setter
    def rotation_matrix(self, r: Union[List[list], np_.ndarray]):
        if not isinstance(r, np_.ndarray):
            r = np_.array(r, dtype=np_.float64)

        if not r.shape == (3, 3):
            raise ValueError('rotation matrix must be of shape (3,3)')

        self.quaternion = np_quaternion.from_rotation_matrix(r)

    @property
    def quaternion(self):
        return self._quaternion

    @quaternion.setter
    def quaternion(self, q: Union[list, np_.ndarray, np_.quaternion]):
        if not isinstance(q, np_.quaternion):
            if not isinstance(q, np_.ndarray):
                q = np_.array(q, dtype=np_.float64)

            q = np_quaternion.from_float_array(q)

        if not q.components.shape == (4,):
            raise ValueError('quaternion must be of shape (4,)')

        self._quaternion = q
