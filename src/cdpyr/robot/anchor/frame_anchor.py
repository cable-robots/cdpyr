from __future__ import annotations

from typing import Optional, Sequence

from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear
)
from cdpyr.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.robot.anchor import anchor as _anchor
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameAnchor(_anchor.Anchor):
    pulley: _pulley.Pulley
    drivetrain: _drivetrain.DriveTrain

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 linear: Optional[_linear.Linear] = None,
                 angular: Optional[_angular.Angular] = None,
                 pulley: Optional[_pulley.Pulley] = None,
                 drivetrain: Optional[_drivetrain.DriveTrain] = None,
                 **kwargs):
        super().__init__(position, dcm, linear, angular, **kwargs)
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


class FrameAnchorList(_anchor.AnchorList, RobotComponent):
    data: Sequence[FrameAnchor]

    @property
    def drivetrain(self):
        return (anchor.drivetrain for anchor in self.data)

    @property
    def pulley(self):
        return (anchor.pulley for anchor in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __hash__(self):
        return hash(tuple(self.data))


__all__ = [
        'FrameAnchor',
        'FrameAnchorList',
]
