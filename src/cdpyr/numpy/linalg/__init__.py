from typing import Sequence, Union

import numpy as _np

from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def issquare(value: Union[Num, Vector, Matrix]):
    value = _np.asarray(value)

    return value.shape[0] == value.shape[1]


def kronecker(size: Sequence, ij: Union[slice, int]):
    """
    Return a Kronecker vector or matrix of a given size with a single entry 1
    and all others zero

    Parameters
    ----------
    size : Sequence
        A numpy valid sequence to create a new array of zeries
    ij : slice | int
        Slice or integer where to place the 1 in the returning kronecker array

    Returns
    -------
    k : numpy.ndarray
        Kronecker array of size `size` with entry/entries at `k[ij] == 1`
    """
    e = _np.zeros(size)
    e[ij] = 1
    return e


def evec_1():
    """
    Unit vector in 2D along the `x`-axis

    Returns
    -------

    """
    return kronecker((2,), 0)


def evec_2():
    """
    Unit vector in 2D along the `y`-axis

    Returns
    -------

    """
    return kronecker((2,), 1)


def evec3_1():
    """
    Unit vector in 3D along the `x`-axis

    Returns
    -------

    """
    return kronecker((3,), 0)


def evec3_2():
    """
    Unit vector in 3D along the `y`-axis

    Returns
    -------

    """
    return kronecker((3,), 1)


def evec3_3():
    """
    Unit vector in 3D along the `3`-axis

    Returns
    -------

    """
    return kronecker((3,), 2)


def cart2pol(x: Union[Num, Vector, Matrix], y: Union[Num, Vector, Matrix]):
    """
    Transform corresponding elements of the two-dimensional Cartesian
    coordinate arrays `x` and `y` into polar coordinates `theta` and `rho`.

    Parameters
    ----------
    x : Num | Vector | Matrix
        Cartesian coordinates. Dimensions must be the same as those of `y` or
        at least properly broadcastable.
    y : Num | Vector | Matrix
        Cartesian coordinates. Dimensions must be the same as those of `x` or
        at least properly broadcastable.

    Returns
    -------
    theta : Num | Vector | Matrix
        Angular coordinate, is the counterclockwise angle in the `x-y` plane
        measured in radians from the positive `x`-axis. The value of the
        angle is in the range `[-numpy.pi, numpy.pi]`.
    rho : Num | Vector | Matrix
        Radial coordinate, is distance from the origin to a point in the
        `x-y` plane measured.

    """
    return _np.arctan2(y, x), _np.hypot(x, y)


def pol2cart(theta: Union[Num, Vector, Matrix],
             rho: Union[Num, Vector, Matrix]):
    """

    Parameters
    ----------
    theta : Num | Vector | Matrix
    rho : Num | Vector | Matrix

    Returns
    -------
    az : Num | Vector | Matrix
    el : Num | Vector | Matrix
    """
    return rho * _np.cos(theta), rho * _np.sin(theta)


def sph2cart(az: Union[Num, Vector, Matrix], el: Union[Num, Vector, Matrix],
             r: Union[Num, Vector, Matrix]):
    """

    Parameters
    ----------
    az : Num | Vector | Matrix
        Azimuth angle, counterclockwise angle in the `x-y` plane measured in
        radians from the positive `x`-axis. The value of the angle is in the
        range `[-numpy.pi, numpy.pi]`. Dimensions must be the same as those
        of `el` and `r` or at least properly broadcastable.
    el : Num | Vector | Matrix
        Elevation angle, is the elevation angle in radians from the `x-y`
        plane. The value of the angle is in the range `[-numpy.pi/2,
        numpy.pi/2]`.  Dimensions must be the same as those of `el` and `r`
        or at least properly broadcastable.
    r : Num | Vector | Matrix
        Radius, is the distance from the origin to a point. The length units
        of `radius`` are arbitrary, matching the units of the input arrays
        `x`, `y`, and `z`.  Dimensions must be the same as those of `el` and
        `r` or at least properly broadcastable.

    Returns
    -------
    x : Num | Vector | Matrix
        Spherical coordinate(s) along the x-axis (or first axis).
    y : Num | Vector | Matrix
        Spherical coordinate(s) along the y-axis (or second axis).
    z : Num | Vector | Matrix
        Spherical coordinate(s) along the z-axis (or third axis).
    """
    return r * _np.cos(el) * _np.cos(az), \
           r * _np.cos(el) * _np.sin(az), \
           r * _np.sin(el)


def cart2sph(x: Union[Num, Vector, Matrix], y: Union[Num, Vector, Matrix],
             z: Union[Num, Vector, Matrix]):
    """
    Transform elements of Cartesian coordinates `(x, y, z)` into their
    spherical coordinates `azimuth`, `elevation`, and `radius`

    Parameters
    ----------
    x : Num | Vector | Matrix
        Spherical coordinate(s) along the x-axis (or first axis). Dimensions
        must be the same as those of `y` and `z` or at least properly
        broadcastable.
    y : Num | Vector | Matrix
        Spherical coordinate(s) along the y-axis (or second axis). Dimensions
        must be the same as those of `y` and `z` or at least properly
        broadcastable.
    z : Num | Vector | Matrix
        Spherical coordinate(s) along the z-axis (or third axis). Dimensions
        must be the same as those of `y` and `z` or at least properly
        broadcastable.

    Returns
    -------
    az : Num | Vector | Matrix
        Azimuth angle, counterclockwise angle in the `x-y` plane measured in
        radians from the positive `x`-axis. The value of the angle is in the
        range `[-numpy.pi, numpy.pi]`.
    el : Num | Vector | Matrix
        Elevation angle, is the elevation angle in radians from the `x-y`
        plane. The value of the angle is in the range `[-numpy.pi/2,
        numpy.pi/2]`.
    r : Num | Vector | Matrix
        Radius, is the distance from the origin to a point. The length units
        of `radius`` are arbitrary, matching the units of the input arrays
        `x`, `y`, and `z`.
    """
    return _np.arctan2(y, x), \
           _np.arctan2(z, _np.sqrt(x ** 2 + y ** 2)), \
           _np.sqrt(x ** 2 + y ** 2 + z ** 2)


__all__ = [
        'cart2pol',
        'cart2sph',
        'evec_1',
        'evec_2',
        'evec3_1',
        'evec3_2',
        'evec3_3',
        'issquare',
        'kronecker',
        'pol2cart',
        'sph2cart',
]
