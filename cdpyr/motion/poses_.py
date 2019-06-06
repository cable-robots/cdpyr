from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

import numpy as np_
from scipy.spatial.transform import Rotation as Rotation_

from cdpyr.kinematics.transform import Angular
from cdpyr.kinematics.transform import Linear


class Pose(object):
    """
    position => (3,)
    orientation => Rotation
    euler => (3,)
    dcm => (3,3)
    rotvec => (3,)
    quaternion => (4,)

    linear_velocity => (3,)
    angular_velocity => (3,)

    linear_acceleration => (3,)
    angular_accceleration => (3,)
    """

    _linear: Linear
    _angular: Angular

    def __init__(self,
                 position: Union[np_.ndarray, list, Iterable, int, float] =
                 None,
                 orientation: Rotation_ = None,
                 quaternion: Union[list, np_.ndarray, Iterable, int, float] =
                 None,
                 dcm: Union[List[list], np_.ndarray, Iterable, int, float] =
                 None,
                 rotvec: Union[list, np_.ndarray, Iterable, int, float] = None,
                 euler: Union[list, np_.ndarray, Iterable, int, float] = None,
                 linear_velocity: Union[
                     list, np_.ndarray, Iterable, int, float] = None,
                 angular_velocity: Union[
                     list, np_.ndarray, Iterable, int, float] = None,
                 linear_acceleration: Union[
                     list, np_.ndarray, Iterable, int, float] = None,
                 angular_acceleration: Union[
                     list, np_.ndarray, Iterable, int, float] = None,
                 time: float = 0
                 ):
        self.linear = Linear(position=position, velocity=linear_velocity,
                             acceleration=linear_acceleration)
        self.angular = Angular(orientation=orientation,
                               quaternion=quaternion, dcm=dcm, rotvec=rotvec,
                               euler=euler, velocity=angular_velocity,
                               acceleration=angular_acceleration)
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
    def linear(self) -> Linear:
        return self._linear

    @linear.setter
    def linear(self, l: Linear):
        self._linear = l

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, a: Angular):
        self._angular = a

    @property
    def position(self):
        return self.linear.linear_position

    @property
    def orientation(self):
        return self.dcm.reshape(9)

    @property
    def dcm(self):
        return self.angular.dcm

    @property
    def quaternion(self):
        return self.angular.quaternion

    @property
    def rotvec(self):
        return self.angular.rotvec

    @property
    def euler(self):
        return self.angular.euler

    def euler(self, seq: str, degrees: Optional[bool] = False):
        return self.angular.euler(seq, degrees=degrees)

    @property
    def linear_velocity(self):
        return self.linear.linear_velocity

    @property
    def angular_velocity(self):
        return self.angular.angular_velocity

    @property
    def linear_acceleration(self):
        return self.linear.linear_acceleration

    @property
    def angular_acceleration(self):
        return self.angular.angular_acceleration

    @property
    def state(self):
        return np_.hstack((self.position, self.quaternion))

    @property
    def pose(self):
        return np_.hstack((self.position, self.orientation))

    def __iter__(self):
        return iter(self.pose)

    def __repr__(self):
        return np_.array2string(np_.hstack([self.time, self.pose]),
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
    def poses(self) -> List[np_.ndarray]:
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
                    el = Pose(position=np_.array(el[1:4]),
                              dcm=np_.array(el[4:], dtype=np_.float64),
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
        return [p.dcm for p in self._poses]

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
