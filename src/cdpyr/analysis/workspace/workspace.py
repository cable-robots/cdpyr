from abc import abstractmethod

from cdpyr.analysis import evaluator as _evaluator, result as _result
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__copyright__ = "Copyright 2019, Philipp Tempel"
__license__ = "EUPL v1.2"


class Algorithm(_evaluator.RobotEvaluator):
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 **kwargs):
        super().__init__(**kwargs)
        self._archetype = archetype
        self._criterion = criterion

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion

    def evaluate(self, robot: '_robot.Robot', *args, parallel=None, **kwargs) -> 'Result':
        try:
            # update keyword arguments with the `parallel` keyword
            kwargs.update({'parallel': parallel})
            # evaluate the workspace
            return self._evaluate(robot, *args, **kwargs)
        except Exception as e:
            raise RuntimeError('Could not determine workspace.') from e

    @abstractmethod
    def _evaluate(self, robot: '_robot.Robot', *args, **kwargs) -> 'Result':
        raise NotImplementedError()


class Result(_result.PlottableResult):
    _algorithm: 'Algorithm'
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'
    _surface_area: float
    _volume: float

    def __init__(self,
                 algorithm: 'Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 **kwargs):
        self._algorithm = algorithm
        self._archetype = archetype
        self._criterion = criterion
        self._surface_area = None
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
    def surface_area(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def volume(self):
        raise NotImplementedError()
