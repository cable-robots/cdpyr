from typing import Union

import numpy as _np

from cdpyr.geometry import cylinder as _cylinder
from cdpyr.geometry.primitive import Primitive
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Tube(Primitive):
    """

    """

    """
    Inner cylinder describing the inside of the tube
    """
    _inner: '_cylinder.Cylinder'

    """
    Outert cylinder describing the ouytside of the tube
    """
    _outer: '_cylinder.Cylinder'

    def __init__(self,
                 inner_radius: Union[Num, Vector],
                 outer_radius: Union[Num, Vector],
                 height: float,
                 center: Vector = None,
                 **kwargs):
        super().__init__(center, **kwargs)
        self._inner = _cylinder.Cylinder(inner_radius, height)
        self._outer = _cylinder.Cylinder(outer_radius, height)

    @property
    def height(self):
        return self._inner.height

    @height.setter
    def height(self, height: float):
        self._inner.height = height
        self._outer.height = height

    @property
    def inner_radius(self):
        return self._inner.radius

    @inner_radius.setter
    def inner_radius(self, radius: Union[Num, Vector]):
        self._inner.radius = radius

    @property
    def outer_radius(self):
        return self._outer.radius

    @outer_radius.setter
    def outer_radius(self, radius: Union[Num, Vector]):
        self._outer.radius = radius

    def _calculate_surface(self):
        return self._inner.surface \
               - 2 * _np.pi * (self._inner.radius[0] * self._inner.radius[1]) \
               + self._outer.surface \
               - 2 * _np.pi * (self._inner.radius[0] * self._inner.radius[1])

    def _calculate_volume(self):
        return self._outer.volume - self._inner.volume


__all__ = [
        'Tube',
]
