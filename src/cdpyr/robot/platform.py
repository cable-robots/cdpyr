from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mixin.list import DispatcherList
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot.anchor import platformanchor as _platformanchor
from cdpyr.typing import Vector


class Platform(object):
    _pose: '_pose.Pose'
    _anchors: '_platformanchor.PlatformAnchorList'
    _center_of_gravity: np_.ndarray
    _center_of_linkage: np_.ndarray
    _motion_pattern: '_motionpattern.Motionpattern'

    def __init__(self,
                 motionpattern: '_motionpattern.Motionpattern',
                 pose: Optional['_pose.Pose'] = None,
                 anchors: Optional[
                     Union['_platformanchor.PlatformAnchorList', Sequence[
                         '_platformanchor.PlatformAnchor']]] = None,
                 center_of_gravity: Vector = None,
                 center_of_linkage: Vector = None
                 ):
        self.anchors = anchors or []
        self.pose = pose or None
        self.center_of_gravity = center_of_gravity or [0.0, 0.0, 0.0]
        self.center_of_linkage = center_of_linkage or [0.0, 0.0, 0.0]
        self.motionpattern = motionpattern

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, pose: '_pose.Pose'):
        self._pose = pose

    @pose.deleter
    def pose(self):
        del self._pose

    @property
    def bi(self):
        return np_.vstack(list(self.anchors.position))

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self,
                anchors: Union['_platformanchor.PlatformAnchorList', Sequence[
                    '_platformanchor.PlatformAnchor']]):
        if not isinstance(anchors, _platformanchor.PlatformAnchorList):
            anchors = _platformanchor.PlatformAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, position: Vector):
        position = np_.asarray(position)

        if not position.ndim == 1:
            raise ValueError(
                'center_of_gravity position must be a 1-dimensional numpy '
                'array, was {}'.format(
                    position.ndim))

        if not position.shape == (3,):
            raise ValueError(
                'center_of_gravity position must be (3,), was {}'.format(
                    position.shape))

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

        if not position.ndim == 1:
            raise ValueError(
                'center_of_linkage position must be a 1-dimensional numpy '
                'array, was {}'.format(
                    position.ndim))

        if not position.shape == (3,):
            raise ValueError(
                'center_of_linkage position must be (3,), was {}'.format(
                    position.shape))

        self._center_of_linkage = position

    @center_of_linkage.deleter
    def center_of_linkage(self):
        del self._center_of_linkage

    @property
    def motionpattern(self):
        return self._motion_pattern

    @motionpattern.setter
    def motionpattern(self, motionpattern: '_motionpattern.Motionpattern'):
        self._motion_pattern = motionpattern

    @motionpattern.deleter
    def motionpattern(self):
        del self._motion_pattern

    def structurematrix(self, pose: '_pose.Pose'):
        return self.motionpattern.structurematrix(self, pose)


Platform.__repr__ = make_repr(
    'motionpattern',
    'pose',
    'anchors',
)


class PlatformList(DispatcherList):

    def __dir__(self):
        return Platform.__dict__.keys()


__all__ = [
    'Platform',
    'PlatformList',
]
