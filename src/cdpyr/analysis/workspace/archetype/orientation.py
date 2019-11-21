import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import generator as _generator, pose as _pose
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Orientation(_archetype.Archetype):

    def __init__(self, position: Vector, step: int = 10):
        self.position = position
        self.step = step
        self.sequence = 'xyz'
        self.euler_min = _np.pi * _np.asarray([-1.0, -1.0, -1.0])
        self.euler_max = _np.pi * _np.asarray([+1.0, +1.0, +1.0])

    @property
    def comparator(self):
        return all

    def _poses(self, coordinate: Vector):
        return _generator.steps(
            _pose.Pose(
                self.position,
                _generator.from_euler(self.sequence, self.euler_min)
            ),
            _pose.Pose(
                self.position,
                _generator.from_euler(self.sequence, self.euler_max)
            ),
            self.step
        )


__all__ = [
    'Orientation',
]
