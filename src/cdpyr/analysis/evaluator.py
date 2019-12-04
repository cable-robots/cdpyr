from abc import ABC, abstractmethod

from cdpyr.motion.pose import pose as _pose, poselist as _poselist
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
    def evaluate(self, robot: '_robot.Robot', *args, **kwargs):
        raise NotImplementedError()


class PoseEvaluator(RobotEvaluator):

    @abstractmethod
    def evaluate(self, robot: '_robot.Robot', pose: '_pose.Pose', *args,
                 **kwargs):
        raise NotImplementedError()


class PoseListEvaluator(RobotEvaluator):

    @abstractmethod
    def evaluate(self, robot: '_robot.Robot', poselist: '_poselist.PoseList',
                 *args, **kwargs):
        raise NotImplementedError()


__all__ = [
        'Evaluator',
        'RobotEvaluator',
        'PoseEvaluator',
        'PoseListEvaluator',
]
