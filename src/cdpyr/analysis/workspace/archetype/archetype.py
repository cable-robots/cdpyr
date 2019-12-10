from abc import ABC, abstractmethod

import numpy as _np

from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Archetype(BaseObject, ABC):

    @property
    @abstractmethod
    def comparator(self):
        raise NotImplementedError()

    def poses(self, coordinate: Vector):
        return self._poses(_np.pad(coordinate, (0, 3 - coordinate.size)))

    @abstractmethod
    def _poses(self, coordinate: Vector):
        raise NotImplementedError()


__all__ = [
        'Archetype'
]
