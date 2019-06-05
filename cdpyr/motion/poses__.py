from typing import List
from typing import Union

import numpy as np_
from scipy import interpolate
from scipy.spatial.transform import Rotation

from cdpyr.traits.angularkinematics import AngularKinematics
from cdpyr.traits.linearkinematics import LinearKinematics


class Pose(LinearKinematics, AngularKinematics):
    """
    Pose object
    """

    """
    Position of the pose
    """
    _position: np_.ndarray

    """
    Orientation object representing the desired orientation in a 
    parametrization independent way
    """
    _orientation: Rotation
    """
    Time value when this value is to be obtained
    """
    _time: float

    def __init__(self,
                 position: Union[list, np_.ndarray, iter],
                 orientation: Rotation = None,
                 euler: Union[list, np_.ndarray, iter] = None,
                 quaternion: Union[list, np_.ndarray, iter] = None,
                 rotvec: Union[list, np_.ndarray, iter] = None,
                 dcm: Union[List[list], np_.ndarray, iter] = None,
                 time: float = 0):
        LinearKinematics.__init__(self, position=position)
        AngularKinematics.__init__(self, orientation=orientation, euler=euler,
                                   quaternion=quaternion, rotvec=rotvec, dcm=dcm)
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
    def pose(self):
        return np_.hstack([self.position, self.dcm.reshape(9)])

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
                    el = Pose(position=np_.array(el[1:4], dtype=np_.float64),
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

    def evaluate(self, t: Union[list, np_.ndarray], *args, **kwargs):
        """
        Evaluate the registered poses at the given time values. If a time
        value does not match a pose's time value, the pose will be
        interpolated in between.

        Position interpolation may be chosen using the second argument, 'kind'

        Orientation interpolation will be done using quaternion slerp.

        :param t:
        :return:
        """

        interpolated_positions = interpolate.interp1d(t, self.positions,
                                                      *args, **kwargs)

    def __repr__(self):
        return '\n'.join(
            ['t,x,y,z,R11,R12,R13,R21,R22,R23,R31,R32,R33'] + [str(p) for p in
                                                               self.poses])
