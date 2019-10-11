from typing import Optional, Sequence, Union, Tuple

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mechanics import inertia as _inertia
from cdpyr.mixin.list import ObjectList
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot.anchor import platformanchor as _platformanchor
from cdpyr.typing import Matrix, Num, Vector


class Platform(object):
    _motion_pattern: '_motionpattern.Motionpattern'
    _anchors: '_platformanchor.PlatformAnchorList'
    _inertia: '_inertia.Inertia'
    _center_of_gravity: np_.ndarray
    _center_of_linkage: np_.ndarray

    def __init__(self,
                 motionpattern: '_motionpattern.Motionpattern',
                 anchors: Optional[Union[
                     '_platformanchor.PlatformAnchorList',
                     Sequence['_platformanchor.PlatformAnchor']
                 ]] = None,
                 inertia: '_inertia.Inertia' = None,
                 center_of_gravity: Vector = None,
                 center_of_linkage: Vector = None
                 ):
        self.anchors = anchors or []
        self.center_of_gravity = center_of_gravity or [0.0, 0.0, 0.0]
        self.center_of_linkage = center_of_linkage or [0.0, 0.0, 0.0]
        self.motionpattern = motionpattern
        self.inertia = inertia if inertia is not None else _inertia.Inertia()

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self,
                anchors: Union[
                    '_platformanchor.PlatformAnchorList',
                    Sequence['_platformanchor.PlatformAnchor']
                ]):
        if not isinstance(anchors, _platformanchor.PlatformAnchorList):
            anchors = _platformanchor.PlatformAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def bi(self):
        return np_.vstack(self.anchors.position).T

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                inertia: Union[
                    Tuple[
                        Union[Num, Vector],
                        Union[Vector, Matrix]
                    ],
                    '_inertia.Inertia'
                ]):
        if not isinstance(inertia, _inertia.Inertia):
            inertia = _inertia.Inertia(inertia[0], inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    @property
    def linear_inertia(self):
        return self.inertia.linear

    @linear_inertia.setter
    def linear_inertia(self, inertia: Union[Num, Vector]):
        self.inertia.linear = inertia

    @property
    def angular_inertia(self):
        return self.inertia.angular

    @angular_inertia.setter
    def angular_inertia(self, inertia: Union[Vector, Matrix]):
        self.inertia.angular = inertia

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, position: Vector):
        position = np_.asarray(position)

        _validator.shape(position, (3,), 'center_of_gravity')

        self._center_of_gravity = position

    @center_of_gravity.deleter
    def center_of_gravity(self):
        del self._center_of_gravity

    @property
    def center_of_linkage(self):
        return self._center_of_linkage

    @center_of_linkage.setter
    def center_of_linkage(self, position: Vector):
        position = np_.asarray(position)

        _validator.shape(position, (3,), 'center_of_linkage')

        self._center_of_linkage = position

    @center_of_linkage.deleter
    def center_of_linkage(self):
        del self._center_of_linkage

    @property
    def motionpattern(self):
        return self._motion_pattern

    @motionpattern.setter
    def motionpattern(self, motionpattern: '_motionpattern.Motionpattern'):
        self._motion_pattern = motionpattern

    @motionpattern.deleter
    def motionpattern(self):
        del self._motion_pattern

    def structurematrix(self, pose: '_pose.Pose'):
        return self.motionpattern.structurematrix(self, pose)


Platform.__repr__ = make_repr(
    'motionpattern',
    'inertia',
    'anchors',
    'center_of_gravity',
    'center_of_linkage',
)


class PlatformList(ObjectList):

    @property
    def __wraps__(self):
        return Platform

    def __dir__(self):
        return Platform.__dict__.keys()


__all__ = [
    'Platform',
    'PlatformList',
]
