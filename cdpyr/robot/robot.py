from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.frame import Frame
from cdpyr.robot.platform import Platform
from cdpyr.motion.pose import Pose

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Robot(object):
    _name: str
    _frame: Frame
    _platforms: Sequence[Platform]

    def __init__(self,
                 name: str = None,
                 frame: Frame = None,
                 platforms: Sequence[Platform] = None):
        self.name = name if name is not None else 'default'
        self.frame = frame if frame is not None else None
        self.platforms = platforms if platforms is not None else []

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
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame: Frame):
        self._frame = frame

    @frame.deleter
    def frame(self):
        del self._frame

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self, platforms: Sequence[Platform]):
        self._platforms = platforms

    @platforms.deleter
    def platforms(self):
        del self._platforms

    @property
    def ai(self):
        return self.frame.ai

    @property
    def bi(self):
        def filter_(p: Platform):
            return p.bi

        return map(filter_, self.platforms)

    @property
    def poses(self):
        def filter_(p: Platform):
            return p.pose

        return map(filter_, self.platforms)

    @poses.setter
    def poses(self, poses: Sequence[Pose]):
        for idx, platform in enumerate(self.platforms):
            platform.pose = poses[idx]

    @poses.deleter
    def poses(self):
        for platform in self.platforms:
            del platform.pose


Robot.__repr__ = make_repr('name', 'frame', 'platforms')

__all__ = ['Robot']
