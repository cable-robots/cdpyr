from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class KinematicsSolver(object):

    @staticmethod
    def forward(algorithm: KinematicAlgorithm, robot: Robot, pose: Pose):
        return algorithm.forward(robot=robot, pose=pose)

    @staticmethod
    def backward(algorithm: KinematicAlgorithm, robot: Robot, pose: Pose):
        return algorithm.backward(robot=robot, pose=pose)


KinematicsSolver.__repr__ = make_repr()

__all__ = ['KinematicsSolver']
