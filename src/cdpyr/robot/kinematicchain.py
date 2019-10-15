from collections import UserList
from typing import Sequence, Union

from magic_repr import make_repr

from cdpyr.robot import (cable as _cable, platform as _platform)
from cdpyr.robot.anchor import (
    frameanchor as _frameanchor,
    platformanchor as _platformanchor,
)
from cdpyr.typing import Num


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


class KinematicChainList(UserList):

    def __init__(self, initlist=None):
        super().__init__()
        # We only support unique kinematic chains i.e., one cable may only be
        # attached to one winch and one platform anchor at a time. That's why
        # we will remove duplicate kinematic chains from the list but in a
        # way that the original order is preserved (FIFO-style).
        # @SEE https://stackoverflow.com/questions/44628186
        seen = set()
        seen_add = seen.add
        self.data = [x for x in initlist if
                     not (x in seen or seen_add(x))] if initlist else []

    @property
    def frame_anchor(self):
        return (kinematicchain.frame_anchor for kinematicchain in self.data)

    @property
    def platform(self):
        return (kinematicchain.platform for kinematicchain in self.data)

    @property
    def platform_anchor(self):
        return (kinematicchain.platform_anchor for kinematicchain in self.data)

    @property
    def cable(self):
        return (kinematicchain.cable for kinematicchain in self.data)

    def with_frame_anchor(self, anchor: '_frameanchor.FrameAnchor'):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__(d for d in self.data if d.frame_anchor in anchor)

    def with_platform(self, platform: '_platform.Platform'):
        platform = platform if isinstance(platform, Sequence) else [platform]

        return self.__class__(d for d in self.data if d.platform in platform)

    def with_platform_anchor(self, anchor: '_platform.Platform'):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__(
            d for d in self.data if d.platform_anchor in anchor)

    def with_cable(self, cable: '_cable.Cable'):
        cable = cable if isinstance(cable, Sequence) else [cable]

        return self.__class__(d for d in self.data if d.cable in cable)


KinematicChainList.__repr__ = make_repr(
    'data'
)

__all__ = [
    'KinematicChain',
    'KinematicChainList',
]
