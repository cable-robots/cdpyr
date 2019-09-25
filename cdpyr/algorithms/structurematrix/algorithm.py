from abc import ABC

from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class StructureMatrixAlgorithm(ABC):

    def calculate(self,
                  robot: Robot,
                  pose: Pose):
        raise NotImplementedError()


StructureMatrixAlgorithm.__repr__ = make_repr()

__all__ = [
    'StructureMatrixAlgorithm'
]
