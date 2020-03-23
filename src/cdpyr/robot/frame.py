from __future__ import annotations

from typing import List, Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear
)
from cdpyr.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.robot.anchor import Anchor, AnchorList
from cdpyr.robot.robot_component import RobotComponent

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

from cdpyr.typing import Vector, Matrix


class Frame(RobotComponent):
    _anchors: FrameAnchorList

    def __init__(self,
                 anchors: Optional[
                     Union[FrameAnchorList, Sequence[
                         FrameAnchor]]] = None,
                 **kwargs):
        """ A general cable robot frame object.

        For the time being, this object only collects all frame anchors and
        provides a nice wrapper around accessing the anchor data.

        :param Union[FrameAnchorList, Sequence[FrameAnchor]] anchors:
        Optional list of anchors or a `FrameAnchorList` available on the frame.
        """
        super().__init__(**kwargs)
        self.anchors = anchors or []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self,
                anchors: Union[FrameAnchorList,
                               Sequence[FrameAnchor]]):
        self._anchors = FrameAnchorList(anchors)

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def ai(self):
        return np_.vstack([anchor.position for anchor in self.anchors]).T

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(
                this == that for this, that in zip(self.anchors, other.anchors))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.anchors)

    __repr__ = make_repr(
            'anchors'
    )


__all__ = [
        'Frame',
]


class FrameAnchor(Anchor):
    pulley: _pulley.Pulley
    drivetrain: _drivetrain.Drivetrain

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 linear: Optional[_linear.Linear] = None,
                 angular: Optional[_angular.Angular] = None,
                 pulley: Optional[_pulley.Pulley] = None,
                 drivetrain: Optional[_drivetrain.Drivetrain] = None,
                 **kwargs):
        super().__init__(position=position,
                         dcm=dcm,
                         linear=linear,
                         angular=angular, **kwargs)
        self.pulley = pulley or None
        self.drivetrain = drivetrain or None

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.pulley == other.pulley \
               and self.drivetrain == other.drivetrain

    def __hash__(self):
        return hash((self.angular, self.drivetrain, self.linear, self.pulley))

    __repr__ = make_repr(
            'position',
            'dcm',
            'pulley',
            'drivetrain',
    )


class FrameAnchorList(AnchorList, RobotComponent):
    data: List[FrameAnchor]

    @property
    def drivetrain(self):
        return (anchor.drivetrain for anchor in self.data)

    @property
    def pulley(self):
        return (anchor.pulley for anchor in self.data)
