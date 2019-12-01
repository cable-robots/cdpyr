import copy
from abc import ABC, abstractmethod
from magic_repr import make_repr

from cdpyr.analysis import result as _result
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

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

        return Result(self, **self._forward(robot, joints, **kwargs))

    direct = forward

    def backward(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose',
                 **kwargs):
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Kinematics are currently not implemented for robots with '
                    'more than one platform.'
            )

        return Result(self, **self._backward(robot, pose, **kwargs))

    inverse = backward

    @abstractmethod
    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Matrix,
                 **kwargs) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> dict:
        raise NotImplementedError()


class Result(_result.PoseResult, _result.PlottableResult):
    _algorithm: 'Algorithm'
    _directions: Matrix
    _joints: Vector
    _swivel: Vector
    _wrap: Vector

    def __init__(self,
                 algorithm: 'Algorithm',
                 pose: '_pose.Pose',
                 joints: Vector,
                 directions: Matrix,
                 swivel: Vector = None,
                 wrap: Vector = None,
                 **kwargs):
        super().__init__(pose)
        self._algorithm = copy.deepcopy(algorithm)
        self._joints = joints
        self._directions = directions
        self._swivel = swivel
        self._wrap = wrap

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def cable_lengths(self):
        return self.joints

    @property
    def directions(self):
        return self._directions

    @property
    def joints(self):
        return self._joints

    @property
    def lengths(self):
        return self._joints

    @property
    def swivel(self):
        return self._swivel

    @property
    def wrap(self):
        return self._wrap

    __repr__ = make_repr(
            'algorithm',
            'pose',
            'joints',
            'swivel',
            'wrap',
    )


__all__ = [
    'Algorithm',
    'Result',
]
