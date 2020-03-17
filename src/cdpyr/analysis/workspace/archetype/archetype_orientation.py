from __future__ import annotations

from abc import ABC
from typing import Union

import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion import pose as _pose
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ArchetypeOrientation(_archetype.Archetype, ABC):
    """
    A base class for all workspace archetypes that vary the position and
    create a valid rotation matrix set at every position
    """

    euler_max: Vector
    euler_min: Vector
    sequence: str
    steps: int

    def __init__(self,
                 euler_min: Vector,
                 euler_max: Vector,
                 sequence: str,
                 steps: Union[Num, Vector] = 10,
                 **kwargs):
        super().__init__(**kwargs)
        self.sequence = sequence
        self.euler_min = _np.asarray(euler_min)
        self.euler_max = _np.asarray(euler_max)
        self.steps = steps

    def _poses(self, coordinate: Vector):
        return _pose.PoseGenerator.orientation(self.euler_min,
                                               self.euler_max,
                                               self.sequence,
                                               coordinate,
                                               self.steps)


__all__ = [
        'ArchetypeOrientation',
]
