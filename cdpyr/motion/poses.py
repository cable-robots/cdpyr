from typing import List
from typing import Tuple
from typing import Union

import numpy as np
import quaternion as np_quaternion


class Pose(object):
    _position: np.ndarray
    _quaternion: np.quaternion
    _time: float

    def __init__(self, position: np.ndarray = None,
                 rotation_matrix: np.ndarray = None,
                 time: float = 0,
                 quaternion: np.ndarray = None,
                 orientation: np.ndarray = None):

        if position is not None:
            self.position = position
        else:
            self.position = np.zeros(3)

        if quaternion is not None:
            self.quaternion = quaternion
        elif rotation_matrix is not None:
            self.rotation_matrix = rotation_matrix
        elif orientation is not None:
            self.orientation = orientation
        else:
            self.quaternion = np_quaternion.one

        self.time = time

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, t: float):
        if t < 0:
            raise ValueError('time must be a nonnegative.')

        self._time = t

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, p: Union[list, np.ndarray]):
        if not isinstance(p, np.ndarray):
            p = np.array(p, dtype=np.float64)

        if not p.shape == (3,):
            raise ValueError('position must be a 3x1 array.')

        self._position = p

    @property
    def quaternion(self) -> np.quaternion:
        return self._quaternion

    @quaternion.setter
    def quaternion(self, q: Union[list, np.quaternion]):
        if not isinstance(q, np.quaternion):
            q = np_quaternion.from_float_array(q)

        if not q.components.shape == (4,):
            raise ValueError('quaternion must be a 4x1 array.')

        self._quaternion = q

    @property
    def state(self) -> np.ndarray:
        return np.hstack([self.position, self.quaternion])

    @property
    def rotation_matrix(self) -> np.ndarray:
        return np_quaternion.as_rotation_matrix(self.quaternion)

    @rotation_matrix.setter
    def rotation_matrix(self, r: Union[List[list], np.ndarray]):
        if not isinstance(r, np.ndarray):
            r = np.array(r, np.float64)

        if not r.shape == (3, 3):
            raise ValueError('rotation_matrix must be a 3x3 array.')

        self.quaternion = np_quaternion.from_rotation_matrix(r)

    @property
    def orientation(self) -> np.ndarray:
        return self.rotation_matrix.reshape(9)

    @orientation.setter
    def orientation(self, o: Union[list, np.ndarray(9)]):
        if not isinstance(o, np.ndarray):
            o = np.array(o, dtype=np.float64)

        if not o.shape == (9,):
            raise ValueError('orientation must be a 9x1 array.')

        self.rotation_matrix = o.reshape([3, 3])

    @property
    def pose(self) -> np.ndarray:
        return np.hstack([self.position, self.orientation])

    @property
    def pose_tuplee(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.position, self.rotation_matrix

    def __iter__(self):
        return iter(self.pose)

    def __repr__(self):
        return np.array2string(np.hstack([self.time, self.pose]),
                               separator=',',
                               formatter={'float_kind': lambda x: "%.2f" %
                                                                  x})[1:-1]

    def __lt__(self, other):
        try:
            return self.time.__lt__(other.time)
        except AttributeError:
            return self.time.__lt__(other)

    def __le__(self, other):
        try:
            return self.time.__le__(other.time)
        except AttributeError:
            return self.time.__le__(other)

    def __gt__(self, other):
        try:
            return self.time.__gt__(other.time)
        except AttributeError:
            return self.time.__gt__(other)

    def __ge__(self, other):
        try:
            return self.time.__ge__(other.time)
        except AttributeError:
            return self.time.__ge__(other)

    def __eq__(self, other):
        try:
            return self.time.__eq__(other.time)
        except AttributeError:
            return self.time.__eq__(other)

    def __ne__(self, other):
        try:
            return self.time.__ne__(other.time)
        except AttributeError:
            return self.time.__ne__(other)


class PoseList(object):
    _poses: List[Pose]

    def __init__(self, poses: List[Pose] = None):
        if len(poses):
            self.poses = poses
        else:
            self.poses = []

    @property
    def poses(self) -> List[np.ndarray]:
        return [p.pose for p in self._poses]

    @poses.setter
    def poses(self, p: Union[List[list], List[Pose]]):
        # Ensure all entries in p are of type Pose, and for those who aren't,
        # we will assume it's a list that we will convert to a pose
        for idx, el in enumerate(p):
            # If entry is not a POSE object, make it one
            if not isinstance(el, Pose):
                # Convert the simple list object to a pose entry
                try:
                    el = Pose(position=np.array(el[1:4]),
                              orientation=np.array(el[4:], dtype=np.float64),
                              time=el[0])
                except TypeError as e:
                    raise TypeError(
                        'pose list entry {} is neither a pose nor a list '
                        'object'.format(idx)
                    ) from e
                finally:
                    p[idx] = el

        self._poses = sorted(p)

    @property
    def times(self):
        return [p.time for p in self._poses]

    @property
    def positions(self):
        return [p.position for p in self._poses]

    @property
    def orientations(self):
        return [p.orientation for p in self._poses]

    @property
    def rotation_matrices(self):
        return [p.rotation_matrix for p in self._poses]

    @property
    def states(self):
        return [p.state for p in self._poses]

    @property
    def quaternions(self):
        return [p.quaternion for p in self._poses]

    def __repr__(self):
        return '\n'.join(
            ['t,x,y,z,R11,R12,R13,R21,R22,R23,R31,R32,R33'] + [str(p) for p in
                                                               self.poses])
