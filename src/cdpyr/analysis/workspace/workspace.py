import copy
from abc import ABC, abstractmethod

from cdpyr.analysis import result as _result
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__copyright__ = "Copyright 2019, Philipp Tempel"
__license__ = "EUPL v1.2"


class Algorithm(ABC):
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self._archetype = archetype
        self._criterion = criterion

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion

    def evaluate(self, robot: '_robot.Robot') -> 'Result':
        try:
            # now finally, evaluate the workspace
            return self._evaluate(robot)
        except BaseException as BaseE:
            raise RuntimeError('Could not determine workspace.') from BaseE

    @abstractmethod
    def _evaluate(self, robot: '_robot.Robot') -> 'Result':
        raise NotImplementedError()


class Result(_result.PlottableResult):
    _algorithm: 'Algorithm'
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'
    _surface: float
    _volume: float

    def __init__(self,
                 algorithm: 'Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self._algorithm = copy.deepcopy(algorithm)
        self._archetype = copy.deepcopy(archetype)
        self._criterion = copy.deepcopy(criterion)
        self._surface = None
        self._volume = None

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion

    @property
    @abstractmethod
    def surface(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def volume(self):
        raise NotImplementedError()
