from abc import ABC, abstractmethod

from cdpyr.analysis.kinematics import result as _result
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(ABC):

    def forward(self,
                robot: '_robot.Robot',
                joints: Matrix,
                **kwargs):
        if robot.num_platforms > 1:
            raise NotImplementedError(
                'Kinematics are currently not implemented for robots with '
                'more than one platform.'
            )

        return _result.Result(
            self,
            **self._forward(robot, joints, **kwargs)
        )

    def direct(self,
               robot: '_robot.Robot',
               joints: Matrix,
               **kwargs):
        return self.forward(robot, joints, **kwargs)

    def backward(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose',
                 **kwargs):
        if robot.num_platforms > 1:
            raise NotImplementedError(
                'Kinematics are currently not implemented for robots with '
                'more than one platform.'
            )

        return _result.Result(
            self,
            **self._backward(robot, pose, **kwargs)
        )

    def inverse(self,
                robot: '_robot.Robot',
                pose: '_pose.Pose',
                **kwargs):
        return self.backward(robot, pose, **kwargs)

    @abstractmethod
    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Matrix,
                 **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> dict:
        raise NotImplementedError


__all__ = [
    'Algorithm',
]
