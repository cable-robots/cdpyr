from abc import ABC

from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class KinematicAlgorithm(ABC):

    def forward(self,
                robot: Robot,
                pose: Pose
                ):
        raise NotImplementedError

    def backward(self,
                 robot: Robot,
                 pose: Pose
                 ):
        raise NotImplementedError


KinematicAlgorithm.__repr__ = make_repr()

__all__ = [
    'KinematicAlgorithm'
]
