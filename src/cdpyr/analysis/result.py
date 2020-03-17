from __future__ import annotations

from abc import ABC

from magic_repr import make_repr

from cdpyr.motion import pose as pose_
from cdpyr.robot import robot as robot_

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):

    def __init__(self, **kwargs):
        pass


class PlottableResult(Result):
    pass


class RobotResult(Result):
    _robot: robot_.Robot

    def __init__(self, robot: robot_.Robot, **kwargs):
        super().__init__(**kwargs)
        self._robot = robot

    @property
    def robot(self):
        return self._robot


class PoseResult(Result):
    _pose: pose_.Pose

    def __init__(self, pose: pose_.Pose, **kwargs):
        super().__init__(**kwargs)
        self._pose = pose

    @property
    def pose(self):
        return self._pose

    __repr__ = make_repr(
            'pose'
    )


class PoseListResult(Result):
    _pose_list: pose_.PoseList

    def __init__(self, pose_list: pose_.PoseList, **kwargs):
        super().__init__(**kwargs)
        self._pose_list = pose_list

    @property
    def pose_list(self):
        return self._pose_list

    __repr__ = make_repr(
            'pose_list'
    )


__all__ = [
        'PlottableResult',
        'PoseResult',
        'PoseListResult',
        'Result',
        'RobotResult',
]
