from abc import ABC
from typing import Sequence

from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class KinematicAlgorithm(ABC):

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

    def _validate_inputs(self, robot: Robot, pose: Pose):
        # turn single entry poses into something iterable
        poses = pose if isinstance(pose, Sequence) else [pose]

        # we need as many poses as we have platforms
        if len(robot.platforms) != len(poses):
            raise ValueError(
                'number of poses must match the number of platforms')

    def _validate_inputs_forward(self, robot: Robot, pose: Pose):
        self._validate_inputs(robot=robot, pose=pose)

    def _validate_inputs_backward(self, robot: Robot, pose: Pose):
        self._validate_inputs(robot=robot, pose=pose)


KinematicAlgorithm.__repr__ = make_repr()

__all__ = [
    'KinematicAlgorithm'
]
