from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'PlottableResult',
        'PoseResult',
        'PoseListResult',
        'Result',
        'RobotResult',
]

from abc import ABC

from magic_repr import make_repr

from cdpyr.motion.pose import Pose, PoseList
from cdpyr.robot.robot import Robot


class Result(ABC):

    def __init__(self, **kwargs):
        pass


class PlottableResult(Result):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class RobotResult(Result):
    _robot: Robot

    def __init__(self, robot: Robot, **kwargs):
        super().__init__(**kwargs)
        self._robot = robot

    @property
    def robot(self):
        return self._robot


class PoseResult(Result):
    _pose: Pose

    def __init__(self, pose: Pose, **kwargs):
        super().__init__(**kwargs)
        self._pose = pose

    @property
    def pose(self):
        return self._pose

    __repr__ = make_repr(
            'pose'
    )


class PoseListResult(Result):
    _pose_list: PoseList

    def __init__(self, pose_list: PoseList, **kwargs):
        super().__init__(**kwargs)
        self._pose_list = pose_list

    @property
    def pose_list(self):
        return self._pose_list

    __repr__ = make_repr(
            'pose_list'
    )
