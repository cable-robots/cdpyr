import copy
from abc import ABC

from cdpyr.motion.pose import pose as _pose, poselist as _poselist
from cdpyr.robot import robot as _robot
from magic_repr import make_repr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):

    def __init__(self, **kwargs):
        pass


class PlottableResult(Result):
    pass


class RobotResult(Result):
    _robot: '_robot.Robot'

    def __init__(self, robot: '_robot.Robot', **kwargs):
        super().__init__(**kwargs)
        self._robot = copy.deepcopy(robot)

    @property
    def robot(self):
        return self._robot


class PoseResult(RobotResult):
    _pose: '_pose.Pose'

    def __init__(self, robot: '_robot.Robot', pose: '_pose.Pose', **kwargs):
        super().__init__(robot=robot, **kwargs)
        self._pose = copy.deepcopy(pose)

    @property
    def pose(self):
        return self._pose

    __repr__ = make_repr(
            'pose'
    )


class PoseListResult(RobotResult):
    _pose_list: '_poselist.PoseList'

    def __init__(self, robot: '_robot.Robot', pose_list: '_poselist.PoseList', **kwargs):
        super().__init__(robot=robot, **kwargs)
        self._pose_list = copy.deepcopy(pose_list)

    @property
    def pose_list(self):
        return self._pose_list

    __repr__ = make_repr(
            'pose_list'
    )


__all__ = [
        'PlottableResult',
        'PoseListResult',
        'PoseResult',
        'Result',
        'RobotResult',
]
