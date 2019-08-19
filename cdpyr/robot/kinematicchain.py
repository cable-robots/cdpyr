from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mixins.lists import DispatcherList
from cdpyr.robot.anchor.frameanchor import FrameAnchor
from cdpyr.robot.anchor.platformanchor import PlatformAnchor
from cdpyr.robot.cable import Cable
from cdpyr.robot.platform import Platform

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


KinematicChain.__repr__ = make_repr(
    'frame_anchor',
    'platform',
    'platform_anchor',
    'cable'
)


class KinematicChainList(DispatcherList):

    def __init__(self, initlist=None):
        super().__init__()
        self.data = list(set(initlist)) if initlist else []

    def __dir__(self):
        return KinematicChain.__dict__.keys()


__all__ = ['KinematicChain', 'KinematicChainList']
