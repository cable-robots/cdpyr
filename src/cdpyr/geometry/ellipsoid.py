from typing import Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry import primitive as _geometry
from cdpyr.typing import Num, Vector

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'


class Ellipsoid(_geometry.Primitive):
    """

    """

    """
    (3,) vector of radii of the ellipsoid along the (X, Y, Z) axes.
    """
    _radius: Vector

    """
    Axis of revolution of the ellipsoid. Allows to also form torus objects
    using the same class. Defaults to `0` i.e., a proper ellipsoid.
    """
    axis: Num

    def __init__(self, radius: Union[Num, Vector], center: Vector = None,
                 axis: Num = 0, **kwargs):
        super().__init__(center, **kwargs)
        self.radius = radius
        self.axis = axis or 0

    @property
    def diameters(self):
        return 2 * self._radius

    @diameters.setter
    def diameters(self, diameter: Union[Num, Vector]):
        # ensure a numpy array, otherwise the halvening won't work
        self.radius = _np.asarray(diameter) / 2

    @diameters.deleter
    def diameters(self):
        del self._radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radii: Union[Num, Vector]):
        radii = _np.asarray(radii)
        if radii.ndim == 0:
            radii = _np.asarray([radii])

        # if a scalar radius is given, we will repeat it three times such
        # that is per X, Y, Z coordinate
        if radii.size == 1:
            radii = _np.repeat(radii, 3, axis=0)

        self._radius = radii

    @radius.deleter
    def radius(self):
        del self._radius

    @property
    def centroid(self):
        return self.center

    @property
    def surface_area(self):
        # currently, I do not have a solution for a generally ellipsoidal
        # torus, so we will just raise an error
        # TODO find a proper math implementation without the complete
        #  elliptic integral of the first kind
        if self.axis:
            raise NotImplementedError()

        # we use Knud Thomsen's formula which requires the power parameter,
        # we set that to this value for a good approximation
        p = 1.6075
        # extract the three radii
        a, b, c = self._radius

        # and apply Knud Thomsen's formula
        return 4.0 * _np.pi * (
                ((a * b) ** p + (a * c) ** p + (b * c) ** p) / 3.0) ** (
                       1.0 / p)

    @property
    def volume(self):
        # currently, I do not have a solution for a generally ellipsoidal
        # torus, so we will just raise an error
        if self.axis:
            raise NotImplementedError()

        return 4.0 / 3.0 * _np.pi * _np.product(self._radius)

    def __hash__(self):
        radii = self.radius
        centroid = self.centroid
        return hash((radii[0], radii[1], radii[2], centroid[0], centroid[1],
                     centroid[2]))

    __repr__ = make_repr(
            'radii',
            'axis',
            'centroid',
            'surface',
            'volume',
    )


__all__ = [
        'Ellipsoid'
]
