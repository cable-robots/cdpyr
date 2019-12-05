from typing import AnyStr, Dict, Iterable, Optional, Sequence, Tuple, Union, Mapping

import numpy as _np
from magic_repr import make_repr

from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import (
    cable as _cable,
    frame as _frame,
    kinematicchain as _kinematicchain,
    platform as _platform
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
    home_pose: '_pose.Pose'

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
                 gravity: Union[Num, Vector] = None,
                 home_pose: '_pose.Pose' = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.name = name or 'default'
        self.frame = frame or None
        self.platforms = platforms or []
        self.cables = cables or []
        self.kinematic_chains = kinematic_chains or {}
        self.gravity = gravity if gravity is not None else [0]
        self.home_pose = home_pose if home_pose is not None else _pose.Pose()

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
                             Sequence['_kinematicchain.KinematicChain'],
                             '_kinematicchain.KinematicChainList',
                             Sequence[Tuple[int, int, int, int]],
                             Sequence[Dict[AnyStr, int]]]):
        if isinstance(chains, Iterable) \
                and not isinstance(chains, _kinematicchain.KinematicChainList):
            # loop over each chain
            for idx, chain in enumerate(chains):
                # deal with chain as dictionary
                if isinstance(chain, Mapping):
                    cable = chain['cable']
                    frame_anchor = chain['frame_anchor']
                    platform_anchor = chain['platform_anchor']
                    try:
                        platform = chain['platform']
                    except KeyError:
                        platform = 0
                else:
                    try:
                        frame_anchor, platform, platform_anchor, cable = chain
                    except ValueError:
                        frame_anchor, platform_anchor, cable = chain
                        platform = 0
                chains[idx] = _kinematicchain.KinematicChain(frame_anchor,
                                                             platform,
                                                             platform_anchor,
                                                             cable)

        # set final value
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
