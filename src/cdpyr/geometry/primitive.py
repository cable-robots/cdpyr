from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as _np
from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Primitive(BaseObject, ABC):
    """

    """

    """
    (3,) vector denoting the point where the geometry primitive is centered
    around
    """
    _center: Vector
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

    def __init__(self, center: Vector = None, **kwargs):
        super().__init__(**kwargs)
        self.center = center if center is not None else [0.0, 0.0, 0.]
        self._centroid = None

    @property
    @abstractmethod
    def centroid(self):
        """
        (3,) vector denoting the centroid of the geometry

        Returns
        -------

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def surface_area(self):
        """
        Surface area of the geometry

        Returns
        -------

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def volume(self):
        """
        Geometric volume of the geometry

        Returns
        -------

        """
        raise NotImplementedError()

    @property
    def center(self):
        """
        (3,) vector denoting the point where the geometry primitive is
        centered around

        Returns
        -------

        """
        return self._center

    @center.setter
    def center(self, center: Vector):
        self._center = _np.asarray(center)

    @center.deleter
    def center(self):
        del self._center

    @property
    def faces(self):
        raise NotImplementedError()

    @property
    def num_faces(self):
        return len(self.faces)

    @property
    def num_vertices(self):
        return len(self.vertices)

    @property
    def vertices(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        if self is other:
            return True

        return _np.allclose(self.centroid, other.centroid) \
               and _np.isclose(self.surface_area, other.surface_area) \
               and _np.isclose(self.volume, other.volume)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        centroid = self.centroid
        return hash((centroid[0], centroid[1], centroid[2], self.surface_area,
                     self.volume))

    __repr__ = make_repr(
            'centroid',
            'surface',
            'volume',
    )


__all__ = [
        'Primitive',
]
