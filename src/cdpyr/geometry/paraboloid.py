from typing import Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry import primitive

__author__ = 'Philipp Tempel'
__email__ = 'phtempel@fastmail.com'
__version__ = '1.0.0-dev'
__license__ = 'EUPL'
__copyright__ = '2019 Philipp Tempel'
__status__ = 'Prototype'

from cdpyr.typing import Num, Vector


class Paraboloid(primitive.Primitive):
    """

    """

    """
    (2,) vector of radii of the paraboloid in the (XZ, YZ) planes
    """
    _radii: Vector

    def __init__(self, radius: Union[Num, Vector], height: Num,
                 center: Vector = None, **kwargs):
        super().__init__(center, **kwargs)
        self.height = height
        self.radius = radius

    @property
    def diameters(self):
        return 2 * self._radii

    @diameters.setter
    def diameters(self, diameter: Union[Num, Vector]):
        # ensure a numpy array, otherwise the halvening won't work
        self.radius = _np.asarray(diameter) / 2

    @diameters.deleter
    def diameters(self):
        del self._radii

    @property
    def radius(self):
        return self._radii

    @radius.setter
    def radius(self, radii: Union[Num, Vector]):
        radii = _np.asarray(radii)
        if radii.ndim == 0:
            radii = _np.asarray([radii])

        # if a scalar radius is given, we will repeat it three times such
        # that is per X, Y, Z coordinate
        if radii.size == 1:
            radii = _np.repeat(radii, 3, axis=0)

        self._radii = radii

    @radius.deleter
    def radius(self):
        del self._radii

    @property
    def shape(self):
        theta = _np.linspace(0, 2 * _np.pi, num=36, endpoint=True)

        # get both radii
        a, b = self._radii

        # linearly space the radii
        ra = _np.linspace(0, a, num=10, endpoint=True)
        rb = _np.linspace(0, b, num=10, endpoint=True)
        # linearly space the rotation
        theta = _np.linspace(0, 2 * _np.pi, num=36, endpoint=True)
        # calculate `x` and `y` coordinates from polar coordinates
        x = _np.outer(ra, _np.cos(theta))
        y = _np.outer(rb, _np.sin(theta))

        # right off, create the result by in-place calculating the height
        return _np.stack((x, y, ((x / a) ** 2 + (y / b) ** 2) * self.height),
                         axis=0)

    def _calculate_surface(self):
        raise NotImplementedError()

    def _calculate_volume(self):
        raise NotImplementedError()

    __repr__ = make_repr(
            'radii',
            'centroid',
            'surface',
            'volume',
    )


__all__ = [
        'Paraboloid'
]
