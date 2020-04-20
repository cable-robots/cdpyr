from __future__ import annotations

from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.exceptions import InvalidPoseException
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Collision(_criterion.Criterion):
    kinematics: _kinematics.Algorithm

    def __init__(self, kinematics: _kinematics.Algorithm, **kwargs):
        super().__init__(**kwargs)
        self.kinematics = kinematics

    def _evaluate(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs):
        raise InvalidPoseException(
                'feature not implemented') from NotImplementedError()


__all__ = [
        'Collision',
]
