from __future__ import annotations

from abc import ABC, abstractmethod

import cdpyr.motion.pose.pose
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Evaluator(ABC):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        raise NotImplementedError()


class RobotEvaluator(Evaluator):

    @abstractmethod
    def evaluate(self, robot: _robot.Robot, *args, **kwargs):
        raise NotImplementedError()


class PoseEvaluator(RobotEvaluator):

    @abstractmethod
    def evaluate(self, robot: _robot.Robot, pose: _pose.Pose, *args,
                 **kwargs):
        raise NotImplementedError()


class PoseListEvaluator(RobotEvaluator):

    @abstractmethod
    def evaluate(self, robot: _robot.Robot, poselist: _pose.PoseList,
                 *args, **kwargs):
        raise NotImplementedError()


__all__ = [
        'Evaluator',
        'RobotEvaluator',
        'PoseEvaluator',
        'PoseListEvaluator',
]
