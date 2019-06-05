from typing import Iterable
from typing import List
from typing import Union

import numpy as np_
from scipy._lib._util import check_random_state
from scipy.spatial.transform import Rotation as Rotation_

from cdpyr.kinematics.transform import Angular
from cdpyr.kinematics.transform import Linear


class Pose(object):
    """
    linear => cdpyr.kinematics.transform.Linear
    angular => cdpyr.kinematics.transform.Angular

    position => (3,)
    orientation => (9,)
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

    @classmethod
    def random(cls, num: int = None, random_state=None):
        random_state = check_random_state(random_state)

        if num is None:
            samples = random_state.normal(size=8)
        else:
            samples = random_state.normal(size=(num, 8))

        return sorted(
            (cls(position=s[1:4], quaternion=s[4:], time=np_.abs(s[0])) for s in
             samples))

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, a: Angular):
        self._angular = a

    @property
    def angular_acceleration(self):
        return self.angular.acceleration

    @property
    def angular_velocity(self):
        return self.angular.velocity

    @property
    def dcm(self):
        return self.angular.dcm

    @property
    def euler(self):
        return self.angular.euler

    @property
    def linear(self) -> Linear:
        return self._linear

    @linear.setter
    def linear(self, l: Linear):
        self._linear = l

    @property
    def linear_acceleration(self):
        return self.linear.acceleration

    @property
    def linear_velocity(self):
        return self.linear.velocity

    @property
    def orientation(self):
        return self.dcm.reshape(9)

    @property
    def pose(self):
        return np_.hstack((self.position, self.orientation))

    @property
    def position(self):
        return self.linear.position

    @property
    def quaternion(self):
        return self.angular.quaternion

    @property
    def rotvec(self):
        return self.angular.rotvec

    @property
    def state(self):
        return np_.hstack((self.position, self.quaternion))

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, t: float):
        if t < 0:
            raise ValueError('time must be nonnegative.')

        self._time = t

    def __iter__(self):
        return iter(self.pose)

    def __str__(self):
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

    @classmethod
    def random(cls, num: int = None, random_state=None):
        random_state = check_random_state(random_state)

        if num is None:
            samples = random_state.normal(size=8)
        else:
            samples = random_state.normal(size=(num, 8))

        return cls(
            [Pose(position=s[1:4], quaternion=s[4:], time=np_.abs(s[0])) for s
             in samples])

    @property
    def dcms(self):
        return [p.dcm for p in self._poses]

    @property
    def euler(self):
        return [p.euler for p in self._poses]

    @property
    def orientations(self):
        return [p.orientation for p in self._poses]

    @property
    def poses(self) -> List[Pose]:
        return self._poses

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
    def positions(self):
        return [p.position for p in self._poses]

    @property
    def quaternions(self):
        return [p.quaternion for p in self._poses]

    @property
    def rotvec(self):
        return [p.rotvec for p in self._poses]

    @property
    def states(self):
        return [p.state for p in self._poses]

    @property
    def times(self):
        return [p.time for p in self._poses]

    def __str__(self):
        return '\n'.join(
            ['t,x,y,z,R11,R12,R13,R21,R22,R23,R31,R32,R33'] + [str(p) for p in
                                                               self.poses])
