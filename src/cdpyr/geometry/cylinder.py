from typing import Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry.primitive import Primitive
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cylinder(Primitive):
    """

    """

    """
    actual height of the cylinder
    """
    height: float
    """
    (2,) vector of the semi radii of the cylinder, which can be either (
    major, minor) or (minor, major)
    """
    _radius: Vector

    def __init__(self, radius: Union[Num, Vector], height: float,
                 center: Vector = None,
                 **kwargs):
        super().__init__(center, **kwargs)
        self.radius = radius
        self.height = height

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius: Union[Num, Vector]):
        radius = _np.asarray(radius)
        if radius.ndim == 0:
            radius = _np.asarray([radius])
        # a single radius means we have a regular cylinder, so we will just
        # repeat the radius for both axes
        if radius.size == 1:
            radius = _np.repeat(radius, 2, axis=0)
        # set result
        self._radius = radius

    @radius.deleter
    def radius(self):
        del self._radius

    @property
    def centroid(self):
        return self.center

    @property
    def surface_area(self):
        # extract semi-major and semi-minor axis lengths
        a, b = self._radius
        # ensure a is the semi-major axis
        if a < b:
            a, b = b, a
        # quicker access to sum and difference of the axes lengths
        apb = a + b
        amb = a - b
        h = (amb ** 2) / (apb ** 2)
        # circumference of the ellipse
        c = _np.pi * apb * (1 + 3 * h / (10 + _np.sqrt(4 - 3 * h)))

        # sum of surface of upper and lower ellipsis and of shell are the total
        # surface
        return 2 * _np.pi * (a * b) + c * self.height

    @property
    def volume(self):
        # simple as that
        return _np.pi * _np.product(self._radius) * self.height

    __repr__ = make_repr(
            'centroid',
            'radius',
            'height',
    )


__all__ = [
        'Cylinder',
]
