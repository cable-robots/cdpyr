import numpy as _np

from cdpyr.analysis.kinematics import kinematics as _algorithm
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import kinematicchain as _kinematicchain, robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pulley(_algorithm.Algorithm):

    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Vector,
                 **kwargs) -> dict:
        raise NotImplementedError()

    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> dict:
        raise NotImplementedError


__all__ = [
    'Pulley',
]
