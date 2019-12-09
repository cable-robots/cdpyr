from collections import UserList
from typing import Sequence, Union

from magic_repr import make_repr

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicChain(RobotComponent):
    cable: int
    frame_anchor: int
    platform: int
    platform_anchor: int

    def __init__(self,
                 frame_anchor: int,
                 platform: int,
                 platform_anchor: int,
                 cable: int,
                 **kwargs):
        super().__init__(**kwargs)
        self.cable = cable
        self.frame_anchor = frame_anchor
        self.platform = platform
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
    data: Sequence[KinematicChain]

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

    def with_frame_anchor(self, anchor: Union[Sequence[Num], Vector]):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__(d for d in self.data if d.frame_anchor in anchor)

    def with_platform(self, platform: Union[Sequence[Num], Vector]):
        platform = platform if isinstance(platform, Sequence) else [platform]

        return self.__class__(d for d in self.data if d.platform in platform)

    def with_platform_anchor(self, anchor: Union[Sequence[Num], Vector]):
        anchor = anchor if isinstance(anchor, Sequence) else [anchor]

        return self.__class__(
                d for d in self.data if d.platform_anchor in anchor)

    def with_cable(self, cable: Union[Sequence[Num], Vector]):
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

    def __hash__(self):
        return hash(tuple(self.data))

    __repr__ = make_repr(
            'data'
    )


__all__ = [
        'KinematicChain',
        'KinematicChainList',
]
