from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class KinematicsSolver(object):

    @staticmethod
    def forward(algorithm: KinematicAlgorithm, robot: Robot, pose: Pose):
        return algorithm.forward(robot=robot, pose=pose)

    @staticmethod
    def backward(algorithm: KinematicAlgorithm, robot: Robot, pose: Pose):
        return algorithm.backward(robot=robot, pose=pose)


KinematicsSolver.__repr__ = make_repr()

__all__ = [
    'KinematicsSolver'
]
