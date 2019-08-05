from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.anchor.platformanchor import PlatformAnchor

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Platform(object):
    _pose: Pose
    _anchors: Sequence[PlatformAnchor]

    def __init__(self,
                 pose: Pose = None,
                 anchors: Sequence[PlatformAnchor] = None
                 ):
        self.anchors = anchors if anchors is not None else []
        self.pose = pose if pose is not None else None

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
        def filter_(a: PlatformAnchor):
            return a.position

        return np_.vstack(list(map(filter_, self.anchors)))

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: Sequence[PlatformAnchor]):
        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors


Platform.__repr__ = make_repr('anchors', 'pose')

__all__ = ['Platform']
