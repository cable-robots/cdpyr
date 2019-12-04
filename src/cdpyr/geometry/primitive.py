from abc import ABC

import numpy as _np
from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

from cdpyr.typing import Vector


class Primitive(ABC, BaseObject):
    """

    """

    """
    (3,) vector denoting the centroid of the geometry
    """
    _centroid: Vector
    """
    Surface area of the geometry
    """
    _surface: float
    """
    Geometric volume of the geometry
    """
    _volume: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._centroid = None
        self._surface = None
        self._volume = None

    @property
    def centroid(self):
        if self._centroid is None:
            self._centroid = self._calculate_centroid()
        return self._centroid

    @property
    def surface(self):
        if self._surface is None:
            self._surface = self._calculate_surface()
        return self._surface

    @property
    def volume(self):
        if self._volume is None:
            self._volume = self._calculate_volume()
        return self._volume

    def _calculate_centroid(self):
        raise NotImplementedError()

    def _calculate_surface(self):
        raise NotImplementedError()

    def _calculate_volume(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        if self is other:
            return True

        return _np.allclose(self.centroid, other.centroid) \
               and _np.isclose(self.surface, other.surface) \
               and _np.isclose(self.volume, other.volume)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        centroid = self.centroid
        return hash((centroid[0], centroid[1], centroid[2], self.surface,
                     self.volume))

    __repr__ = make_repr(
            'centroid',
            'surface',
            'volume',
    )


__all__ = [
        'Primitive',
]
