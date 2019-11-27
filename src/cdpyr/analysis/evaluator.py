from abc import (
    ABC,
    abstractmethod
)

from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, robot: '_robot.Robot', *args, **kwargs):
        raise NotImplementedError


__all__ = [
    'Evaluator',
]
