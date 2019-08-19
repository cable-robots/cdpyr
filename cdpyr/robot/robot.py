from typing import Dict, List, Optional, Sequence, Set, Tuple, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.motion.pose import Pose
from cdpyr.robot.anchor.frameanchor import FrameAnchor
from cdpyr.robot.anchor.platformanchor import PlatformAnchor
from cdpyr.robot.cable import Cable, CableList, CableSchema
from cdpyr.robot.frame import Frame, FrameSchema
from cdpyr.robot.kinematicchain import (
    KinematicChain,
    KinematicChainList,
    KinematicChainSchema,
)
from cdpyr.robot.platform import Platform, PlatformList, PlatformSchema

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Robot(object):
    _name: str
    _frame: Frame
    _platforms: PlatformList
    _cables: CableList
    _chains: KinematicChainList

    def __init__(self,
                 name: Optional[str] = None,
                 frame: Optional[Frame] = None,
                 platforms: Optional[
                     Union[PlatformList, Sequence[Platform]]] = None,
                 cables: Optional[Union[CableList, Sequence[Cable]]] = None,
                 kinematic_chains: Optional[Union[KinematicChainList, Set[
                     Union[Sequence[_TNum], KinematicChain]]]] = None
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
    def frame(self, frame: Frame):
        self._frame = frame

    @frame.deleter
    def frame(self):
        del self._frame

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self, platforms: Union[PlatformList, Sequence[Platform]]):
        if not isinstance(platforms, PlatformList):
            platforms = PlatformList(platforms)

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

    @property
    def poses(self):
        return list(self.platforms.pose)

    @poses.setter
    def poses(self, poses: Sequence[Pose]):
        self.platforms.pose = poses

    @poses.deleter
    def poses(self):
        for platform in self.platforms:
            del platform.pose

    @property
    def cables(self):
        return self._cables

    @cables.setter
    def cables(self, cables: Union[CableList, Sequence[Cable]]):
        if not isinstance(cables, CableList):
            cables = CableList(cables)

        self._cables = cables

    @cables.deleter
    def cables(self):
        del self._cables

    @property
    def kinematic_chains(self):
        return self._chains

    @kinematic_chains.setter
    def kinematic_chains(self,
                         chains: Union[KinematicChainList, Set[
                             Union[Sequence[_TNum], KinematicChain]]]):
        # turn anything not a set into a set (also removes already redundant
        # objects)
        if not isinstance(chains, Set):
            chains = set(chains)

        # loop over each chain and turn it from integer values into object
        # values
        for idx, v in enumerate(chains):
            if not isinstance(v, KinematicChain):
                # remove from the list
                chains.remove(v)

                # create a proper KinematicChain object
                if isinstance(v, Dict):
                    frame_anchor = v['frame_anchor']
                    platform = v['platform']
                    platform_anchor = v['platform_anchor']
                    cable = v['cable']
                elif isinstance(v, List) or isinstance(v, Tuple):
                    frame_anchor, platform, platform_anchor, cable = v

                if not isinstance(frame_anchor, FrameAnchor):
                    frame_anchor = self.frame.anchors[frame_anchor]

                if not isinstance(platform, Platform):
                    platform = self.platforms[platform]

                if not isinstance(platform_anchor, PlatformAnchor):
                    platform_anchor = self.platforms[self.platforms.index(
                        platform)].anchors[platform_anchor]

                if not isinstance(cable, Cable):
                    cable = self.cables[cable]

                chains.add(KinematicChain(
                    frame_anchor=frame_anchor,
                    platform=platform,
                    platform_anchor=platform_anchor,
                    cable=cable
                ))

        # and set the correct object type
        self._chains = KinematicChainList(chains)

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


class RobotSchema(Schema):
    name = fields.Str()
    frame = fields.Nested(FrameSchema)
    platforms = fields.List(fields.Nested(PlatformSchema))
    cables = fields.List(fields.Nested(CableSchema))
    kinematic_chains = fields.List(fields.Nested(KinematicChainSchema))

    __model__ = Robot

    @post_load
    def make_robot(self, data):
        return self.__model__(**data)


__all__ = ['Robot', 'RobotSchema']
