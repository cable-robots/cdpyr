from abc import ABC
from typing import Sequence

from magic_repr import make_repr

from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot


class Algorithm(ABC):

    def forward(self,
                robot: '_robot.Robot',
                pose: '_pose.Pose'
                ):
        """

        Parameters
        ----------
        robot: Robot
            A robot object that contains frame anchors and platforms
        pose: Pose

        """
        raise NotImplementedError()

    def backward(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose'
                 ):
        raise NotImplementedError()

    def _validate_inputs(self, robot: '_robot.Robot', pose: '_pose.Pose'):
        # turn single entry pose into something iterable
        poses = pose if isinstance(pose, Sequence) else [pose]

        # we need as many pose as we have platforms
        if len(robot.platforms) != len(poses):
            raise ValueError(
                'number of pose must match the number of platforms')

    def _validate_inputs_forward(self, robot: '_robot.Robot',
                                 pose: '_pose.Pose'):
        self._validate_inputs(robot=robot, pose=pose)

    def _validate_inputs_backward(self, robot: '_robot.Robot',
                                  pose: '_pose.Pose'):
        self._validate_inputs(robot=robot, pose=pose)


Algorithm.__repr__ = make_repr()

__all__ = [
    'Algorithm'
]
