from magic_repr import make_repr

from typing import Union, Sequence

from cdpyr.mixin.list import DispatcherList
from cdpyr.typing import Num

from cdpyr.robot import (
    platform as _platform,
    cable as _cable
)
from cdpyr.robot.anchor import frameanchor as _frameanchor
from cdpyr.robot.anchor import  platformanchor as _platformanchor


class KinematicChain(object):
    _cable: '_cable.Cable'
    _platform: '_platform.Platform'
    _frame_anchor: '_frameanchor.FrameAnchor'
    _platform_anchor: '_platformanchor.PlatformAnchor'

    def __init__(self,
                 frame_anchor: Union['_frameanchor.FrameAnchor', Num],
                 platform: Union['_platform.Platform', Num],
                 platform_anchor: Union['_platformanchor.PlatformAnchor', Num],
                 cable: Union['_cable.Cable', Num]
                 ):
        self.cable = cable
        self.platform = platform
        self.frame_anchor = frame_anchor
        self.platform_anchor = platform_anchor

    @property
    def cable(self):
        return self._cable

    @cable.setter
    def cable(self, cable: Union['_cable.Cable', Num]):
        self._cable = cable

    @cable.deleter
    def cable(self):
        del self._cable

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform: Union['_platform.Platform', Num]):
        self._platform = platform

    @platform.deleter
    def platform(self):
        del self._platform

    @property
    def frame_anchor(self):
        return self._frame_anchor

    @frame_anchor.setter
    def frame_anchor(self, anchor: Union['_frameanchor.FrameAnchor', Num]):
        self._frame_anchor = anchor

    @frame_anchor.deleter
    def frame_anchor(self):
        del self._frame_anchor

    @property
    def platform_anchor(self):
        return self._platform_anchor

    @platform_anchor.setter
    def platform_anchor(self, anchor: Union['_platform.Platform', Num]):
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

    def with_frame_anchor(self, anchor: '_frameanchor.FrameAnchor'):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__([d for d in self.data if d.frame_anchor in anchor])

    def with_platform(self, platform: '_platform.Platform'):
        platform = platform if isinstance(platform, Sequence) else [platform]

        return self.__class__([d for d in self.data if d.platform in platform])

    def with_platform_anchor(self, anchor: '_platform.Platform'):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__([d for d in self.data if d.platform_anchor in anchor])

    def with_cable(self, cable: '_cable.Cable'):
        cable = cable if isinstance(cable, Sequence) else [cable]

        return self.__class__([d for d in self.data if d.cable in cable])


__all__ = [
    'KinematicChain',
    'KinematicChainList',
]
