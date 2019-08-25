from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class PulleyKinematics(KinematicAlgorithm):

    def forward(self,
                robot: Robot,
                pose: Pose
                ):
        raise NotImplementedError()
    def backward(self,
                 robot: Robot,
                 pose: Pose
                 ):
        raise NotImplementedError()

PulleyKinematics.__repr__ = make_repr()

__all__ = [
    'PulleyKinematics'
]
