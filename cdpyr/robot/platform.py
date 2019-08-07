from typing import Optional
from typing import Sequence
from typing import Union

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

    def __init__(self,
                 pose: Optional[Pose] = None,
                 anchors: Optional[Union[PlatformAnchorList, Sequence[
                     PlatformAnchor]]] = None
                 ):
        self.anchors = anchors or []
        self.pose = pose or None

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
    def anchors(self, anchors: Union[PlatformAnchorList, Sequence[
        PlatformAnchor]]):
        if not isinstance(anchors, PlatformAnchorList):
            anchors = PlatformAnchorList(anchors)

        self._anchors = PlatformAnchorList(anchors)

    @anchors.deleter
    def anchors(self):
        del self._anchors


Platform.__repr__ = make_repr(
    'anchors',
    'pose'
)


class PlatformList(DispatcherList):
    pass


__all__ = ['Platform', 'PlatformList']
