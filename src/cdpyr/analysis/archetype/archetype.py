from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Archetype',
        'ArchetypeOrientation',
]

from abc import ABC, abstractmethod
from typing import Union

import numpy as _np

from cdpyr.base import CdpyrObject
from cdpyr.motion import pose as _pose
from cdpyr.typing import Num, Vector


class Archetype(CdpyrObject, ABC):

    @property
    @abstractmethod
    def comparator(self):
        raise NotImplementedError()

    @property
    def name(self):
        return self.__class__.__name__

    def poses(self, coordinate: Vector):
        return self._poses(_np.pad(coordinate, (0, 3 - coordinate.size)))

    @abstractmethod
    def _poses(self, coordinate: Vector):
        raise NotImplementedError()


class ArchetypeOrientation(Archetype, ABC):
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
