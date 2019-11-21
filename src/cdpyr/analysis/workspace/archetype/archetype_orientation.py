import numpy as _np
from abc import ABC

from cdpyr import validator as _validator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import generator as _generator, pose as _pose
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ArchetypeOrientation(_archetype.Archetype, ABC):
    _sequence: str
    _step: int
    _euler_min: Vector
    _euler_max: Vector

    def __init__(self,
                 euler_min: Vector,
                 euler_max: Vector,
                 sequence: str,
                 step: int = 10):
        self.sequence = sequence
        self.euler_min = _np.asarray(euler_min)
        self.euler_max = _np.asarray(euler_max)
        self.step = step

    @property
    def euler_min(self):
        return self._euler_min

    @euler_min.setter
    def euler_min(self, euler_min: Vector):
        euler_min = _np.asarray(euler_min)
        _validator.data.length(euler_min, len(self.sequence), 'euler_min')
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
        _validator.data.length(euler_max, len(self.sequence), 'euler_max')
        self._euler_max = euler_max

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
    def step(self):
        return self._step

    @step.setter
    def step(self, step: int):
        _validator.numeric.greater_than(step, 0, 'step')

        self._step = step

    @step.deleter
    def step(self):
        del self._step

    def _poses(self, coordinate: Vector):
        return _generator.steps(
            _pose.Pose(
                coordinate,
                _generator.from_euler(self._sequence, self._euler_min)
            ),
            _pose.Pose(
                coordinate,
                _generator.from_euler(self._sequence, self._euler_max)
            ),
            self._step
        )


__all__ = [
    'ArchetypeOrientation',
]
