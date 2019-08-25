from enum import Enum

from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.algorithms.kinematics.pulley import PulleyKinematics
from cdpyr.algorithms.kinematics.standard import StandardKinematics
from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class Solver(Enum):
    STANDARD = (StandardKinematics())
    PULLEY = (PulleyKinematics())

    _algorithm: KinematicAlgorithm

    def __init__(self,
                 algorithm: KinematicAlgorithm):
        self.algorithm = algorithm

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: KinematicAlgorithm):
        self._algorithm = algorithm

    @algorithm.deleter
    def algorithm(self):
        del self._algorithm

    def forward(self,
                robot: Robot,
                pose: Pose
                ):
        return self.algorithm.forward(robot=robot, pose=pose)

    def backward(self,
                 robot: Robot,
                 pose: Pose
                 ):
        return self.algorithm.backward(robot=robot, pose=pose)


Solver.__repr__ = make_repr()

__all__ = [
    'Solver'
]
