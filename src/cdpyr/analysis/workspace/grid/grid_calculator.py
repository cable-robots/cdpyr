import itertools
from typing import Union

import numpy as _np

from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace import (
    algorithm as _algorithm,
)
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.grid import grid_result as _result
from cdpyr.robot import robot as _robot
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GridCalculator(_algorithm.Algorithm):
    _lower_bound: Vector
    _upper_bound: Vector
    _steps: Vector

    def __init__(self,
                 # kinematics: '_kinematics.Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 lower_bound: Union[Num, Vector] = None,
                 upper_bound: Union[Num, Vector] = None,
                 steps: Union[Num, Vector] = None):
        super().__init__(archetype, criterion)
        self.lower_bound = lower_bound if lower_bound is not None else [0]
        self.upper_bound = upper_bound if upper_bound is not None else [0]
        self.steps = steps if steps is not None else [1]

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, bound: Union[Num, Vector]):
        bound = _np.asarray(bound)
        if bound.ndim == 0:
            bound = _np.asarray([bound])

        self._lower_bound = bound

    @lower_bound.deleter
    def lower_bound(self):
        del self._lower_bound

    @property
    def upper_bound(self):
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, bound: Union[Num, Vector]):
        bound = _np.asarray(bound)
        if bound.ndim == 0:
            bound = _np.asarray([bound])

        self._upper_bound = bound

    @upper_bound.deleter
    def upper_bound(self):
        del self._upper_bound

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps: Union[Num, Vector]):
        steps = _np.asarray(steps)
        if steps.ndim == 0:
            steps = _np.asarray([steps])

        if steps.size != self._lower_bound.size:
            steps = _np.repeat(steps, self._lower_bound.size - (steps.size - 1))[0:self._lower_bound.size]

        self._steps = steps

    def coordinates(self):
        # differences in position
        diff_pos = self._upper_bound - self._lower_bound

        # delta in position to perform per step
        deltas = diff_pos / self._steps
        # set deltas to zero where no step is needed
        deltas[_np.isclose(self._steps, 0)] = 0

        # how many iterations to perform per axis
        iterations = self._steps * _np.logical_not(_np.isclose(diff_pos, 0))

        # return a generator object of coordinates
        return (self._lower_bound + deltas * a for a in itertools.product(
            *(range(0, iterations[k] + 1) for k in range(0, len(iterations)))
        ))

    def _evaluate(self, robot: '_robot.Robot') -> '_result.Result':
        # temporarily store the robot as local property so it won't be passed
        # as method argument on every coordinate evaluation
        self.__robot = robot

        # fancy list comprehension
        coordinates, flags = list(zip(
            *((coordinate, self.__check__coordinate(robot, coordinate)) for
              coordinate in
              self.coordinates())))

        # remove the temporary object
        del self.__robot

        # return the tuple of poses that were evaluated
        return _result.GridResult(
            self,
            self._archetype,
            self._criterion,
            coordinates,
            flags
        )

    def __check__coordinate(self, robot, coordinate: _np.ndarray):
        return self._archetype.comparator(self._criterion.evaluate(robot, pose)
                                         for pose in
                                         self._archetype.poses(coordinate))


__all__ = [
    'GridCalculator',
]
