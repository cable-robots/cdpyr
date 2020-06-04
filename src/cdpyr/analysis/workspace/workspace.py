from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Algorithm',
        'Result',
]

from abc import abstractmethod

from cdpyr.analysis import evaluator as _evaluator, result as _result
from cdpyr.analysis.archetype import archetype as _archetype_
from cdpyr.analysis.criterion import criterion as _criterion_
from cdpyr.robot import robot as _robot


class Algorithm(_evaluator.RobotEvaluator):
    _archetype: _archetype_.Archetype
    _criterion: _criterion_.Criterion

    def __init__(self,
                 archetype: _archetype_.Archetype,
                 criterion: _criterion_.Criterion,
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

    def evaluate(self,
                 robot: _robot.Robot,
                 *args,
                 parallel=None,
                 **kwargs) -> Result:
        try:
            # update keyword arguments with the `parallel` keyword
            kwargs.update({'parallel': parallel})
            # evaluate the workspace
            return self._evaluate(robot, *args, **kwargs)
        except Exception as e:
            raise RuntimeError('Could not determine workspace.') from e

    @abstractmethod
    def _evaluate(self,
                  robot: _robot.Robot,
                  *args,
                  **kwargs) -> Result:
        raise NotImplementedError()


class Result(_result.PlottableResult):
    _algorithm: Algorithm
    _archetype: _archetype_.Archetype
    _criterion: _criterion_.Criterion
    _surface_area: float
    _volume: float

    def __init__(self,
                 algorithm: Algorithm,
                 archetype: _archetype_.Archetype,
                 criterion: _criterion_.Criterion,
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

    @abstractmethod
    def to_poselist(self):
        raise NotImplementedError()
