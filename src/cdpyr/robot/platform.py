import itertools
from collections import UserList
from typing import Optional, Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mechanics import inertia as _inertia
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motion_pattern as _motion_pattern
from cdpyr.robot.anchor import platform_anchor as _platform_anchor
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Platform(object):
    _anchors: '_platform_anchor.PlatformAnchorList'
    _center_of_gravity: 'np_.ndarray'
    _center_of_linkage: 'np_.ndarray'
    _inertia: '_inertia.Inertia'
    _motion_pattern: '_motion_pattern.MotionPattern'
    _name: str
    _pose: '_pose.Pose'

    def __init__(self,
                 motion_pattern: '_motion_pattern.MotionPattern',
                 anchors: Optional[Union[
                     '_platform_anchor.PlatformAnchorList',
                     Sequence['_platform_anchor.PlatformAnchor']
                 ]] = None,
                 inertia: Optional['_inertia.Inertia'] = None,
                 center_of_gravity: Optional[Vector] = None,
                 center_of_linkage: Optional[Vector] = None,
                 name: str = None
                 ):
        self.anchors = anchors or []
        self.center_of_gravity = center_of_gravity or [0.0, 0.0, 0.0]
        self.center_of_linkage = center_of_linkage or [0.0, 0.0, 0.0]
        self.motion_pattern = motion_pattern
        self.inertia = inertia if inertia is not None else _inertia.Inertia()
        self.pose = _pose.Pose()
        self.name = name or 'default'

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self,
                anchors: Union[
                    '_platform_anchor.PlatformAnchorList',
                    Sequence['_platform_anchor.PlatformAnchor']
                ]):
        if not isinstance(anchors, _platform_anchor.PlatformAnchorList):
            anchors = _platform_anchor.PlatformAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def angular_inertia(self):
        return self.inertia.angular

    @angular_inertia.setter
    def angular_inertia(self, inertia: Matrix):
        self.inertia.angular = inertia

    @property
    def bi(self):
        return np_.vstack([anchor.position for anchor in self.anchors]).T

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, position: Vector):
        position = np_.asarray(position)

        _validator.linalg.shape(position, (3,), 'center_of_gravity')

        self._center_of_gravity = position

    @center_of_gravity.deleter
    def center_of_gravity(self):
        del self._center_of_gravity

    @property
    def center_of_linkage(self):
        return self._center_of_linkage

    @center_of_linkage.setter
    def center_of_linkage(self, position: Vector):
        position = np_.asarray(position)

        _validator.linalg.shape(position, (3,), 'center_of_linkage')

        self._center_of_linkage = position

    @center_of_linkage.deleter
    def center_of_linkage(self):
        del self._center_of_linkage

    @property
    def dof(self):
        return self.motion_pattern.dof

    @property
    def dof_rotation(self):
        return self.motion_pattern.dof_rotation

    @property
    def dof_translation(self):
        return self.motion_pattern.dof_translation

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                inertia: Union[
                    Tuple[Vector, Matrix],
                    '_inertia.Inertia'
                ]):
        if not isinstance(inertia, _inertia.Inertia):
            inertia = _inertia.Inertia(inertia[0], inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    @property
    def linear_inertia(self):
        return self.inertia.linear

    @linear_inertia.setter
    def linear_inertia(self, inertia: Matrix):
        self.inertia.linear = inertia

    @property
    def motion_pattern(self):
        return self._motion_pattern

    @motion_pattern.setter
    def motion_pattern(self, motion_pattern: '_motion_pattern.MotionPattern'):
        self._motion_pattern = motion_pattern

    @motion_pattern.deleter
    def motion_pattern(self):
        del self._motion_pattern

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, pose: '_pose.Pose'):
        self._pose = pose

    @pose.deleter
    def pose(self):
        del self._pose

    def wrench(self,
               pose: '_pose.Pose' = None,
               gravity: Optional[Union[Num, Vector]] = None):
        # get rotation matrix from the given or internal pose
        dcm = (pose if pose is not None else self.pose).angular.dcm

        # pass down to the motion pattern for handling
        return self.motion_pattern.wrench(self.inertia.linear,
                                          self.motion_pattern.gravity(gravity),
                                          dcm,
                                          self.center_of_gravity)


Platform.__repr__ = make_repr(
    'anchors',
    'center_of_gravity',
    'center_of_linkage',
    'inertia',
    'motion_pattern',
    'pose',
)


class PlatformList(UserList):

    @property
    def all_combinations(self):
        return itertools.combinations_with_replacement(self.data, 2)

    @property
    def anchors(self):
        return (platform.anchors for platform in self.data)

    @property
    def angular_inertia(self):
        return (platform.angular_inertia for platform in self.data)

    @property
    def center_of_gravity(self):
        return (platform.center_of_gravity for platform in self.data)

    @property
    def center_of_linkage(self):
        return (platform.center_of_linkage for platform in self.data)

    @property
    def inertia(self):
        return (platform.inertia for platform in self.data)

    @property
    def linear_inertia(self):
        return (platform.linear_inertia for platform in self.data)

    @property
    def motion_pattern(self):
        return (platform.motion_pattern for platform in self.data)


PlatformList.__repr__ = make_repr(
    'data'
)

__all__ = [
    'Platform',
    'PlatformList',
]
