from __future__ import annotations

import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation
from cdpyr.motion import generator as _generator
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Orientation(_archetype_orientation.ArchetypeOrientation):
    """
    The `Orientation` workspace is given through the poses with
        the rotations in SO3
    for which
        the position is fixed in R3
    and the observed criterion is valid
    """

    def __init__(self, position: Vector, steps: int = 10, **kwargs):
        euler = _np.pi * _np.asarray([+1.0, +1.0, +1.0])
        super().__init__(-euler, +euler, 'xyz', steps, **kwargs)
        self.position = position

    @property
    def comparator(self):
        return all

    def _poses(self, *args, **kwargs):
        return _generator.orientation(self.euler_min,
                                      self.euler_max,
                                      self.sequence,
                                      self.position,
                                      self.steps)


__all__ = [
        'Orientation',
]
