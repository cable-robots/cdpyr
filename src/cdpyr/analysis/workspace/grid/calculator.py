import itertools
from typing import Union

import numpy as _np

from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace import (
    algorithm as _algorithm,
)
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.grid import result as _result
from cdpyr.robot import robot as _robot
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Calculator(_algorithm.Algorithm):
    _lower_bound: Vector
    _upper_bound: Vector
    _step: Vector

    def __init__(self,
                 kinematics: '_kinematics.Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 lower_bound: Union[Num, Vector] = None,
                 upper_bound: Union[Num, Vector] = None,
                 step: Union[Num, Vector] = None):
        super().__init__(kinematics, archetype, criterion)
        self.lower_bound = lower_bound if lower_bound is not None else [0]
        self.upper_bound = upper_bound if upper_bound is not None else [0]
        self.step = step if step is not None else [1]

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
    def step(self):
        return self._step

    @step.setter
    def step(self, step: Union[Num, Vector]):
        step = _np.asarray(step)
        if step.ndim == 0:
            step = _np.asarray([step])

        self._step = step

    def coordinates(self):
        # differences in position
        diff_pos = self.upper_bound - self.lower_bound

        # delta in position to perform per step
        deltas = diff_pos / self.step
        # set deltas to zero where no step is needed
        deltas[_np.isclose(self.step, 0)] = 0

        # how many iterations to perform per axis
        iterations = self.step * _np.logical_not(_np.isclose(diff_pos, 0))

        # return a generator object of coordinates
        return (self.lower_bound + deltas * a for a in itertools.product(
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
        return _result.Result(
            self,
            self.archetype,
            self.criterion,
            coordinates,
            flags
        )

    def _validate(self, robot: '_robot.Robot'):
        pass

    def __check__coordinate(self, robot, coordinate: _np.ndarray):
        return self.archetype.comparator(self.criterion.evaluate(robot, pose)
                                         for pose in
                                         self.archetype.poses(coordinate))


__all__ = [
    'Calculator',
]
