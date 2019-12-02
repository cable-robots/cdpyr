import copy
from abc import ABC, abstractmethod
from typing import Union

import numpy as _np

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
    """

    """

    """
    Algorithm used for calculation of the kinematics result
    """
    _algorithm: 'Algorithm'
    """
    `(M,)` of swivel angles of each cable frame
    """
    _swivel: Vector
    """
    `(M,)` of wrap angles of each pulley
    """
    _wrap: Vector

    """
    `(NT, M)` array of unit cable direction vectors
    """
    _directions: Matrix

    """
    `(2, M)` array where each column consists of `[workspace, pulley]` lengths
    """
    _lengths: Matrix

    def __init__(self, algorithm: 'Algorithm', pose: '_pose.Pose',
                 lengths: Union[Vector, Matrix],
                 directions: Matrix,
                 swivel: Vector = None,
                 wrap: Vector = None):
        super().__init__(pose)
        self._algorithm = copy.deepcopy(algorithm)
        lengths = _np.asarray(lengths)
        self._lengths = lengths if lengths.ndim == 2 else lengths[None, :]
        self._directions = _np.asarray(directions)
        self._swivel = _np.asarray(swivel)
        self._wrap = _np.asarray(wrap)

    @property
    def lengths(self):
        return self.joints

    @property
    def directions(self):
        return self._directions

    @property
    def joints(self):
        return _np.sum(self._lengths, axis=0)

    @property
    def swivel_angles(self):
        return self._swivel

    @property
    def workspace_length(self):
        return self._lengths[0, :]

    @property
    def wrapped_length(self):
        try:
            return self._lengths[1, :]
        except IndexError:
            return None

    @property
    def wrap_angles(self):
        return self._wrap


__all__ = [
        'Algorithm',
        'Result',
]
