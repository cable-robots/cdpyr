from enum import Enum

from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm import (
    Pulley,
    Standard,
)
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot


class Kinematics(Enum):
    STANDARD = (Standard())
    PULLEY = (Pulley())

    @property
    def algorithm(self):
        return self._value_

    def forward(self,
                robot: '_robot.Robot',
                pose: '_pose.Pose'
                ):
        return self.algorithm.forward(robot=robot, pose=pose)

    def backward(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose'
                 ):
        return self.algorithm.backward(robot=robot, pose=pose)


Kinematics.__repr__ = make_repr()

__all__ = [
    'Kinematics'
]
