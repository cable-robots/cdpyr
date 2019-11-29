from collections import UserList
from typing import (
    Sequence,
    Union,
)

from magic_repr import make_repr

from cdpyr.robot import (
    cable as _cable,
    platform as _platform,
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor,
)
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicChain(RobotComponent):
    cable: '_cable.Cable'
    platform: '_platform.Platform'
    frame_anchor: '_frame_anchor.FrameAnchor'
    platform_anchor: '_platform_anchor.PlatformAnchor'

    def __init__(self,
                 frame_anchor: Union['_frame_anchor.FrameAnchor', Num],
                 platform: Union['_platform.Platform', Num],
                 platform_anchor: Union['_platform_anchor.PlatformAnchor', Num],
                 cable: Union['_cable.Cable', Num]
                 ):
        self.cable = cable
        self.platform = platform
        self.frame_anchor = frame_anchor
        self.platform_anchor = platform_anchor

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.frame_anchor == other.frame_anchor \
               and self.platform == other.platform \
               and self.platform_anchor == other.platform_anchor \
               and self.cable == other.cable

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.cable,
                     self.frame_anchor,
                     self.platform,
                     self.platform_anchor))

    __repr__ = make_repr(
        'frame_anchor',
        'platform',
        'platform_anchor',
        'cable'
    )


class KinematicChainList(UserList, RobotComponent):

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

    def with_frame_anchor(self, anchor: '_frame_anchor.FrameAnchor'):
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
    'KinematicChain',
    'KinematicChainList',
]
