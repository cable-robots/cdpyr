from typing import Dict, List, Optional, Sequence, Set, Tuple, Union

from magic_repr import make_repr

from cdpyr.robot import (
    cable as _cable,
    frame as _frame,
    kinematicchain as _kinematicchain,
    platform as _platform,
)
from cdpyr.robot.anchor import (
    frameanchor as _frameanchor,
    platformanchor as _platformanchor,
)


class Robot(object):
    _name: str
    _frame: '_frame.Frame'
    _platforms: '_platform.PlatformList'
    _cables: '_cable.CableList'
    _chains: '_kinematicchain.KinematicChainList'

    def __init__(self,
                 name: Optional[str] = None,
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
                     Set[Dict[str, int]]
                 ]] = None
                 ):
        self.name = name or 'default'
        self.frame = frame or None
        self.platforms = platforms or []
        self.cables = cables or []
        self.kinematic_chains = kinematic_chains or {}

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
    def frame(self, frame: '_frame.Frame'):
        self._frame = frame

    @frame.deleter
    def frame(self):
        del self._frame

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self,
                  platforms: Union[
                      '_platform.PlatformList',
                      Sequence['_platform.Platform']
                  ]):
        if not isinstance(platforms, _platform.PlatformList):
            platforms = _platform.PlatformList(platforms)

        self._platforms = platforms

    @platforms.deleter
    def platforms(self):
        del self._platforms

    @property
    def ai(self):
        return self.frame.ai

    @property
    def bi(self):
        return list(self.platforms.bi)

    # @property
    # def poses(self):
    #     return list(self.platforms.pose)
    #
    # @poses.setter
    # def poses(self,
    #           poses: Sequence['_pose.Pose']):
    #     self.platforms.pose = poses

    # @poses.deleter
    # def poses(self):
    #     for platform in self.platforms:
    #         del platform.pose

    @property
    def cables(self):
        return self._cables

    @cables.setter
    def cables(self,
               cables: Union[
                   '_cable.CableList',
                   Sequence['_cable.Cable']
               ]):
        if not isinstance(cables, _cable.CableList):
            cables = _cable.CableList(cables)

        self._cables = cables

    @cables.deleter
    def cables(self):
        del self._cables

    @property
    def kinematic_chains(self):
        return self._chains

    @kinematic_chains.setter
    def kinematic_chains(self,
                         chains: Union[
                             '_kinematicchain.KinematicChainList',
                             Sequence['_kinematicchain.KinematicChain'],
                             Sequence[Tuple[int, int, int, int]],
                             Sequence[Dict[str, int]]
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
                    platform = v['platform']
                    platform_anchor = v['platform_anchor']
                    cable = v['cable']
                elif isinstance(v, List) or isinstance(v, Tuple):
                    frame_anchor, platform, platform_anchor, cable = v

                if not isinstance(frame_anchor, _frameanchor.FrameAnchor):
                    frame_anchor = self.frame.anchors[frame_anchor]

                if not isinstance(platform, _platform.Platform):
                    platform = self.platforms[platform]

                if not isinstance(platform_anchor,
                                  _platformanchor.PlatformAnchor):
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

        # and set the correct object type
        self._chains = _kinematicchain.KinematicChainList(chains)

    @kinematic_chains.deleter
    def kinematic_chains(self):
        del self._chains


Robot.__repr__ = make_repr(
    'name',
    'frame',
    'platforms',
    'cables',
    'kinematic_chains'
)

__all__ = [
    'Robot',
]
