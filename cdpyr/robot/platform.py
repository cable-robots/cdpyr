from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mixins.lists import DispatcherList
from cdpyr.motion.pose import Pose
from cdpyr.robot.anchor.platformanchor import PlatformAnchor
from cdpyr.robot.anchor.platformanchor import PlatformAnchorList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Platform(object):
    _pose: Pose
    _anchors: PlatformAnchorList
    _center_of_gravity: np_.ndarray
    _center_of_linkage: np_.ndarray

    def __init__(self,
                 pose: Optional[Pose] = None,
                 anchors: Optional[Union[PlatformAnchorList, Sequence[
                     PlatformAnchor]]] = None,
                 center_of_gravity: _TVector = None,
                 center_of_linkage: _TVector = None
                 ):
        self.anchors = anchors or []
        self.pose = pose or None
        self.center_of_gravity = center_of_gravity or [0.0, 0.0, 0.0]
        self.center_of_linkage = center_of_linkage or [0.0, 0.0, 0.0]

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, pose: Pose):
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
                anchors: Union[PlatformAnchorList, Sequence[PlatformAnchor]]):
        if not isinstance(anchors, PlatformAnchorList):
            anchors = PlatformAnchorList(anchors)

        self._anchors = PlatformAnchorList(anchors)

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, position: _TVector):
        position = np_.asarray(position)

        if not position.shape == (3,):
            raise ValueError('invalid shape of center_of_gravity; must be (3,'
                             '), was {}'.format(position.shape))

        self._center_of_gravity = position

    @center_of_gravity.deleter
    def center_of_gravity(self):
        del self._center_of_gravity

    @property
    def center_of_linkage(self):
        return self._center_of_linkage

    @center_of_linkage.setter
    def center_of_linkage(self, position: _TVector):
        position = np_.asarray(position)

        if not position.shape == (3,):
            raise ValueError('invalid shape of center_of_linkage; must be (3,'
                             '), was {}'.format(position.shape))

        self._center_of_linkage = position

    @center_of_linkage.deleter
    def center_of_linkage(self):
        del self._center_of_linkage


Platform.__repr__ = make_repr(
    'anchors',
    'pose'
)


class PlatformList(DispatcherList):

    def __dir__(self):
        return Platform.__dict__.keys()


__all__ = ['Platform', 'PlatformList']
