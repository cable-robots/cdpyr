from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Evaluator',
        'RobotEvaluator',
        'PoseEvaluator',
        'PoseListEvaluator',
]

from abc import abstractmethod

from cdpyr.base import Algorithm
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot


class Evaluator(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def evaluate(self,
                 *args,
                 **kwargs):
        raise NotImplementedError()


class RobotEvaluator(Evaluator):

    @abstractmethod
    def evaluate(self,
                 robot: _robot.Robot,
                 *args,
                 **kwargs):
        raise NotImplementedError()


class PoseEvaluator(Evaluator):

    @abstractmethod
    def evaluate(self,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 *args,
                 **kwargs):
        raise NotImplementedError()


class PoseListEvaluator(Evaluator):

    @abstractmethod
    def evaluate(self,
                 robot: _robot.Robot,
                 pose_list: _pose.PoseList,
                 *args,
                 **kwargs):
        raise NotImplementedError()
