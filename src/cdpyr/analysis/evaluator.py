from abc import abstractmethod

from cdpyr.analysis import evaluator as _evaluator
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__copyright__ = "Copyright 2019, Philipp Tempel"
__license__ = "EUPL v1.2"


class Evaluator(_evaluator.Evaluator):

    @abstractmethod
    def evaluate(self, robot: '_robot.Robot', *args, **kwargs):
        raise NotImplementedError


__all__ = [
    'Evaluator',
]
