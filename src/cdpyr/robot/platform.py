import itertools
from collections import UserList
from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.mechanics import inertia as _inertia
from cdpyr.motion.pattern import pattern as _motion_pattern
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot.anchor import platform_anchor as _platform_anchor
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import (
    Matrix,
    Num,
    Vector,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Platform(RobotComponent):
    _anchors: '_platform_anchor.PlatformAnchorList'
    _center_of_gravity: np_.ndarray
    _center_of_linkage: np_.ndarray
    geometry: '_geometry.Geometry'
    inertia: '_inertia.Inertia'
    motion_pattern: '_motion_pattern.Pattern'
    name: str
    pose: '_pose.Pose'

    def __init__(self,
                 motion_pattern: '_motion_pattern.Pattern',
                 anchors: Optional[Union[
                     '_platform_anchor.PlatformAnchorList',
                     Sequence['_platform_anchor.PlatformAnchor']
                 ]] = None,
                 inertia: Optional['_inertia.Inertia'] = None,
                 center_of_gravity: Optional[Vector] = None,
                 center_of_linkage: Optional[Vector] = None,
                 name: str = None,
                 pose: '_pose.Pose' = None,
                 geometry: '_geometry.Geometry' = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.anchors = anchors or []
        self.center_of_gravity = center_of_gravity or [0.0, 0.0, 0.0]
        self.center_of_linkage = center_of_linkage or [0.0, 0.0, 0.0]
        self.motion_pattern = motion_pattern
        self.inertia = inertia if inertia is not None else _inertia.Inertia()
        self.pose = pose if pose is not None else _pose.Pose()
        self.name = name or 'default'
        self.geometry = geometry

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self,
                anchors: Union[
                    '_platform_anchor.PlatformAnchorList',
                    Sequence['_platform_anchor.PlatformAnchor']
                ]):
        self._anchors = _platform_anchor.PlatformAnchorList(anchors)

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
    def can_rotate(self):
        return self.motion_pattern.can_rotate

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, position: Vector):
        self._center_of_gravity = np_.asarray(position)

    @center_of_gravity.deleter
    def center_of_gravity(self):
        del self._center_of_gravity

    @property
    def center_of_linkage(self):
        return self._center_of_linkage

    @center_of_linkage.setter
    def center_of_linkage(self, position: Vector):
        self._center_of_linkage = np_.asarray(position)

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
    def is_point(self):
        return self.motion_pattern.is_point

    @property
    def is_beam(self):
        return self.motion_pattern.is_beam

    @property
    def is_cuboid(self):
        return self.motion_pattern.is_cuboid

    @property
    def linear_inertia(self):
        return self.inertia.linear

    @linear_inertia.setter
    def linear_inertia(self, inertia: Matrix):
        self.inertia.linear = inertia

    @property
    def moves_linear(self):
        return self.motion_pattern.moves_linear

    @property
    def moves_planar(self):
        return self.motion_pattern.moves_planar

    @property
    def moves_spatial(self):
        return self.motion_pattern.moves_spatial

    @property
    def num_anchors(self):
        return len(self._anchors)

    def gravitational_wrench(self,
                             pose: '_pose.Pose' = None,
                             gravity: Optional[Union[Num, Vector]] = None):
        # get rotation matrix from the given or internal pose
        dcm = (pose if pose is not None else self.pose).angular.dcm

        # pass down to the motion pattern for handling
        return self.motion_pattern.gravitational_wrench(
                self.inertia.linear, self.motion_pattern.gravity(gravity), dcm,
                self.center_of_gravity)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.anchors == other.anchors \
               and np_.allclose(self.center_of_gravity,
                                other.center_of_gravity) \
               and np_.allclose(self.center_of_linkage,
                                other.center_of_linkage) \
               and self.inertia == other.inertia \
               and self.motion_pattern == other.motion_pattern \
               and self.name == other.name \
               and self.pose == other.pose

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.anchors,
                     id(self.center_of_gravity),
                     id(self.center_of_linkage),
                     self.inertia,
                     self.motion_pattern,
                     self.name,
                     self.pose))

    __repr__ = make_repr(
            'anchors',
            'center_of_gravity',
            'center_of_linkage',
            'inertia',
            'motion_pattern',
            'pose',
    )


class PlatformList(UserList, RobotComponent):
    data: Sequence[Platform]

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
    def bi(self):
        return (platform.bi for platform in self.data)

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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __ne__(self, other):
        return not self == other

    __repr__ = make_repr(
            'data'
    )


__all__ = [
        'Platform',
        'PlatformList',
]
