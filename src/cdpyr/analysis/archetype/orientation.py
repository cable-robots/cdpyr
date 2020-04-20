from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Orientation',
]

import numpy as _np

from cdpyr.analysis.archetype import archetype as _archetype
from cdpyr.motion import pose as _pose
from cdpyr.typing import Vector


class Orientation(_archetype.ArchetypeOrientation):
    """
    The `Orientation` workspace is given through the poses with
        the rotations in SO3
    for which
        the position is fixed in R3
    and the observed criterion is valid
    """

    _position: Vector

    def __init__(self, position: Vector, steps: int = 10, **kwargs):
        euler = _np.pi * _np.asarray([+1.0, +1.0, +1.0])
        super().__init__(euler_min=-euler,
                         euler_max=+euler,
                         sequence='xyz',
                         steps=steps,
                         **kwargs)
        self._position = position

    @property
    def comparator(self):
        return all

    @property
    def position(self):
        return self._position

    def _poses(self, *args, **kwargs):
        return _pose.PoseGenerator.orientation(self.euler_min,
                                               self.euler_max,
                                               self.sequence,
                                               self._position,
                                               self.steps)
