import itertools
from typing import Union

import numpy as _np
from abc import ABC

from cdpyr import validator as _validator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import generator as _generator, pose as _pose
from cdpyr.typing import (
    Vector,
    Num
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ArchetypeOrientation(_archetype.Archetype, ABC):
    """
    A base class for all workspace archetypes that vary the position and
    create a valid rotation matrix set at every position
    """

    _sequence: str
    _steps: int
    _euler_min: Vector
    _euler_max: Vector

    def __init__(self,
                 euler_min: Vector,
                 euler_max: Vector,
                 sequence: str,
                 steps: Union[Num, Vector] = 10):
        self.sequence = sequence
        self.euler_min = _np.asarray(euler_min)
        self.euler_max = _np.asarray(euler_max)
        self.steps = steps

    @property
    def euler_min(self):
        return self._euler_min

    @euler_min.setter
    def euler_min(self, euler_min: Vector):
        euler_min = _np.asarray(euler_min)
        _validator.data.length(euler_min, len(self._sequence), 'euler_min')
        self._euler_min = euler_min

    @euler_min.deleter
    def euler_min(self):
        del self._euler_min

    @property
    def euler_max(self):
        return self._euler_max

    @euler_max.setter
    def euler_max(self, euler_max: Vector):
        euler_max = _np.asarray(euler_max)
        _validator.data.length(euler_max, len(self._sequence), 'euler_max')
        self._euler_max = euler_max - 10 * _np.finfo(euler_max.dtype).eps

    @euler_max.deleter
    def euler_max(self):
        del self._euler_max

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence: str):
        self._sequence = sequence

    @sequence.deleter
    def sequence(self):
        del self._sequence

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps: int):
        _validator.numeric.greater_than(steps, 0, 'steps')

        self._steps = steps

    @steps.deleter
    def steps(self):
        del self._steps

    def _poses(self, coordinate: Vector):
        return _generator.orientation(self._euler_min,
                                      self._euler_max,
                                      self._sequence,
                                      coordinate,
                                      self._steps)


__all__ = [
    'ArchetypeOrientation',
]
