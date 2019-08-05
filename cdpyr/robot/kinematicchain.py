from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.cable import Cable
from cdpyr.robot.frame import FrameAnchor
from cdpyr.robot.platform import Platform
from cdpyr.robot.platform import PlatformAnchor

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class KinematicChain(object):
    _cable: Cable
    _platform: Platform
    _frame_anchor: FrameAnchor
    _platform_anchor: PlatformAnchor

    def __init__(self,
                 frame_anchor: Union[_TNum, FrameAnchor],
                 platform: Union[_TNum, Platform],
                 platform_anchor: Union[_TNum, PlatformAnchor],
                 cable: Union[_TNum, Cable]
                 ):
        self.cable = cable
        self.platform = platform
        self.frame_anchor = frame_anchor
        self.platform_anchor = platform_anchor

    @property
    def cable(self):
        return self._cable

    @cable.setter
    def cable(self, cable: Cable):
        self._cable = cable

    @cable.deleter
    def cable(self):
        del self._cable

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform: Platform):
        self._platform = platform

    @platform.deleter
    def platform(self):
        del self._platform

    @property
    def frame_anchor(self):
        return self._frame_anchor

    @frame_anchor.setter
    def frame_anchor(self, anchor: FrameAnchor):
        self._frame_anchor = anchor

    @frame_anchor.deleter
    def frame_anchor(self):
        del self._frame_anchor

    @property
    def platform_anchor(self):
        return self._platform_anchor

    @platform_anchor.setter
    def platform_anchor(self, anchor: PlatformAnchor):
        self._platform_anchor = anchor

    @platform_anchor.deleter
    def platform_anchor(self):
        del self._platform_anchor


KinematicChain.__repr__ = make_repr('frame_anchor', 'platform',
                                    'platform_anchor', 'cable')

__all__ = ['KinematicChain']
