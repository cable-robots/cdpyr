from typing import (
    AnyStr,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as _np
from magic_repr import make_repr

from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import (
    cable as _cable,
    frame as _frame,
    kinematicchain as _kinematicchain,
    platform as _platform,
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor,
)
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Robot(RobotComponent):
    _cables: '_cable.CableList'
    _chains: '_kinematicchain.KinematicChainList'
    frame: '_frame.Frame'
    _gravity: _np.ndarray
    name: AnyStr
    _platforms: '_platform.PlatformList'

    def __init__(self,
                 name: Optional[AnyStr] = None,
                 frame: Optional['_frame.Frame'] = None,
                 platforms: Optional[Union[
                     '_platform.PlatformList',
                     Sequence['_platform.Platform']
                 ]] = None,
                 cables: Optional[Union[
                     '_cable.CableList',
                     Sequence['_cable.Cable']
                 ]] = None,
                 kinematic_chains: Optional[Union[
                     '_kinematicchain.KinematicChainList',
                     Sequence['_kinematicchain.KinematicChain'],
                     Sequence[Tuple[int, int, int, int]],
                     Sequence[Dict[AnyStr, int]]
                 ]] = None,
                 gravity: Union[Num, Vector] = None
                 ):
        self.name = name or 'default'
        self.frame = frame or None
        self.platforms = platforms or []
        self.cables = cables or []
        self.kinematic_chains = kinematic_chains or {}
        self.gravity = gravity if gravity is not None else [0]

    @property
    def ai(self):
        return self.frame.ai

    @property
    def bi(self):
        return _np.hstack(list(self.platforms.bi))

    @property
    def can_rotate(self):
        return any(platform.can_rotate for platform in self.platforms)

    @property
    def cables(self):
        return self._cables

    @cables.setter
    def cables(self,
               cables: Union['_cable.CableList',
                             Sequence['_cable.Cable']
               ]):
        self._cables = _cable.CableList(cables)

    @cables.deleter
    def cables(self):
        del self._cables

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, gravity: Union[Num, Vector]):
        self._gravity = _np.asarray(gravity)

    @gravity.deleter
    def gravity(self):
        del self._gravity

    @property
    def kinematic_chains(self):
        return self._chains

    @kinematic_chains.setter
    def kinematic_chains(self,
                         chains: Union[
                             '_kinematicchain.KinematicChainList',
                             Sequence['_kinematicchain.KinematicChain'],
                             Sequence[Tuple[int, int, int, int]],
                             Sequence[Dict[AnyStr, int]]
                         ]):
        # turn anything not a set into a set (also removes already redundant
        # objects)
        # if not isinstance(chains, Set) and not isinstance(chains, tuple):
        #     chains = set(chains)

        # loop over each chain and turn it from integer values into object
        # values
        for idx, v in enumerate(chains):
            if not isinstance(v, _kinematicchain.KinematicChain):
                # create a proper KinematicChain object
                if isinstance(v, Dict):
                    frame_anchor = v['frame_anchor']
                    # platform value may be provided, but must not be,
                    # so it defaults to the first platform
                    try:
                        platform = v['platform']
                    except KeyError:
                        platform = 0
                    platform_anchor = v['platform_anchor']
                    cable = v['cable']
                elif isinstance(v, List) or isinstance(v, Tuple):
                    # platform value may be provided, but must not be,
                    # so it defaults to the first platform
                    try:
                        frame_anchor, platform, platform_anchor, cable = v
                    except ValueError:
                        frame_anchor, platform_anchor, cable = v
                        platform = 0

                if not isinstance(frame_anchor, _frame_anchor.FrameAnchor):
                    frame_anchor = self.frame.anchors[frame_anchor]

                if not isinstance(platform, _platform.Platform):
                    platform = self.platforms[platform]

                if not isinstance(platform_anchor,
                                  _platform_anchor.PlatformAnchor):
                    platform_anchor = self.platforms[
                        self.platforms.index(platform)
                    ].anchors[platform_anchor]

                if not isinstance(cable, _cable.Cable):
                    cable = self.cables[cable]

                # update the entry with the correct type i.e., convert
                # anything into KinematicChain which isn't already
                chains[idx] = _kinematicchain.KinematicChain(
                        frame_anchor=frame_anchor,
                        platform=platform,
                        platform_anchor=platform_anchor,
                        cable=cable
                )

        # We only support unique kinematic chains i.e., one cable may only be
        # attached to one winch and one platform anchor at a time. That's why
        # we will remove duplicate kinematic chains from the list but in a
        # way that the original order is preserved (FIFO-style).
        # @SEE https://stackoverflow.com/questions/44628186
        seen = set()
        seen_add = seen.add
        chains = [x for x in chains if not (x in seen or seen_add(x))]

        # and set the correct object type
        self._chains = _kinematicchain.KinematicChainList(chains)

    @kinematic_chains.deleter
    def kinematic_chains(self):
        del self._chains

    @property
    def moves_linear(self):
        return any(platform.moves_linear for platform in self.platforms)

    @property
    def moves_planar(self):
        return any(platform.moves_planar for platform in self.platforms)

    @property
    def moves_spatial(self):
        return any(platform.moves_spatial for platform in self.platforms)

    @property
    def num_cables(self):
        return len(self.cables)

    @property
    def num_dof(self):
        return sum(platform.dof for platform in self.platforms)

    @property
    def num_dof_rotation(self):
        return sum(platform.dof_rotation for platform in self.platforms)

    @property
    def num_dof_translation(self):
        return sum(platform.dof_translation for platform in self.platforms)

    @property
    def num_kinematic_chains(self):
        return len(self.kinematic_chains)

    @property
    def num_platforms(self):
        return len(self.platforms)

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self,
                  platforms: Union[
                      '_platform.PlatformList',
                      Sequence['_platform.Platform']
                  ]):
        self._platforms = _platform.PlatformList(platforms)

    @platforms.deleter
    def platforms(self):
        del self._platforms

    def gravitational_wrench(self, pose: '_pose.Pose'):
        if self.num_platforms > 1:
            raise NotImplementedError(
                    'Wrench calculation is not implemented for robots with '
                    'more than one platforms.')

        return self.platforms[0].gravitational_wrench(pose, self.gravity)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.cables == other.cables \
               and self.frame == other.frame \
               and self.kinematic_chains == other.kinematic_chains \
               and self.name == other.name \
               and self.platforms == other.platforms

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.cables,
                     self.frame,
                     self.kinematic_chains,
                     self.name,
                     self.platforms))

    __repr__ = make_repr(
            'name',
            'frame',
            'platforms',
            'cables',
            'kinematic_chains'
    )


__all__ = [
    'Robot',
]
