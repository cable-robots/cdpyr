from typing import Iterable
from typing import List
from typing import Union

import numpy as np_


class Cube(object):
    _width: float
    _depth: float
    _height: float
    _mass: float
    _linear_inertia: np_.ndarray
    _angular_inertia: np_.ndarray
    _material: str

    def __init__(self,
                 width: float,
                 depth: float = None,
                 height: float = None,
                 mass: float = None,
                 angular_inertia: Union[List[list], np_.ndarray, Iterable, int,
                                        float] = None,
                 material: str = None,
                 *args,
                 **kwargs):

        self.width = width
        self.height = height if height is not None else width
        self.depth = depth if depth is not None else width

        self.mass = mass if mass is not None else 1

        if angular_inertia is not None:
            self.angular_inertia = angular_inertia

        self.material = material if material is not None else 'default'

    @property
    def angular_inertia(self):
        # Cache angular inertia
        if self._angular_inertia is None:
            self._angular_inertia = 1. / 12. * self.mass * np_.diag(
                [self.height ** 2 + self.depth ** 2,
                 self.width ** 2 + self.depth ** 2,
                 self.width ** 2 + self.height ** 2])

        return self._angular_inertia

    @angular_inertia.setter
    def angular_inertia(self, ai: Union[List[list], np_.ndarray, Iterable,
                                        int, float]):
        self._angular_inertia = np_.asarray(ai, dtype=np_.float64)

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, d: float):
        if d < 0:
            raise ValueError('depth must be nonnegative')

        self._depth = d

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h: float):
        if h < 0:
            raise ValueError('height must be nonnegative')

        self._height = h

    @property
    def linear_inertia(self):
        # Cache linear inertia
        if self._linear_inertia is None:
            self._linear_inertia = self.mass * np_.eye(3)

        return self._linear_inertia

    @linear_inertia.setter
    def linear_inertia(self, inertia: Union[list, np_.ndarray, Iterable, int,
                                            float]):

        inertia = np_.asarray(inertia, dtype=np_.float64)

        # Convert scalar inertia into
        if not inertia.shape == (3, 3):
            inertia = np_.eye(3) * inertia[0, 0]

        # Check all inertia entries are greater than zero
        if (inertia < 0).any():
            raise ValueError('linear_inertia must be all positive')

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        self._mass = mass
        self.linear_inertia = mass * np_.eye(3)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: str):
        self._material = material

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w: float):
        if w < 0:
            raise ValueError('width must be nonnegative')

        self._width = w


class Cylinder(object):
    _radius_inner: float
    _radius_outer: float
    _length: float
    _diameter: float
    _mass: float
    _linear_inertia: np_.ndarray
    _angular_inertia: np_.ndarray
    _material: str

    def __init__(self,
                 length: float,
                 radius: float = None,
                 mass: float = None,
                 angular_inertia: Union[List[list], np_.ndarray, Iterable, int,
                                        float] = None,
                 diameter: float = None,
                 radius_inner: float = None,
                 diameter_inner: float = None,
                 material: str = None,
                 *args,
                 **kwargs):
        if radius is None and diameter is None:
            raise AttributeError('missing attribute radius or diameter')

        self.diameter = diameter if diameter is not None else 1
        self.diameter_inner = diameter_inner if diameter_inner is not None \
            else 0

        self.radius = radius if radius is not None else 1
        self.radius_inner = radius_inner if radius is not None else 0

        self.length = length if length is not None else 1
        self.mass = mass if mass is not None else 1
        if angular_inertia is not None:
            self.angular_inertia = angular_inertia

        self.material = material if material is not None else 'default'

    @property
    def angular_inertia(self):
        # Cache angular inertia
        if self._angular_inertia is None:
            r = self.radius_inner ** 2 + self.radius_outer ** 2
            self._angular_inertia = 1. / 12. * self.mass * np_.diag(
                [3 * r + self.length ** 2, 3 * r + self.length ** 2, r])

        return self._angular_inertia

    @angular_inertia.setter
    def angular_inertia(self, ai: Union[List[list], np_.ndarray, Iterable,
                                        int, float]):
        self._angular_inertia = np_.asarray(ai, dtype=np_.float64)

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, length: float):
        if length <= 0:
            raise ValueError('length must be positive')

        self._length = length

    @property
    def linear_inertia(self):
        # Cache linear inertia
        if self._linear_inertia is None:
            self._linear_inertia = self.mass * np_.eye(3)

        return self._linear_inertia

    @linear_inertia.setter
    def linear_inertia(self, inertia: Union[list, np_.ndarray, Iterable, int,
                                            float]):

        inertia = np_.asarray(inertia, dtype=np_.float64)

        # Convert scalar inertia into
        if not inertia.shape == (3, 3):
            inertia = np_.eye(3) * inertia[0, 0]

        # Check all inertia entries are greater than zero
        if (inertia < 0).any():
            raise ValueError('linear_inertia must be all positive')

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        self._mass = mass
        self.linear_inertia = mass * np_.eye(3)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: str):
        self._material = material

    @property
    def radius(self) -> float:
        return self.radius_outer

    @radius.setter
    def radius(self, radius: float):
        self.radius_outer = radius

    @property
    def radius_inner(self) -> float:
        return self._radius_inner

    @radius_inner.setter
    def radius_inner(self, ri: float):
        if ri < 0:
            raise ValueError('radius_inner must be non-negative')

        if ri >= self.radius_outer:
            raise ValueError('radius_inner must be smaller than radius_outer')

        self._radius_inner = ri

    @property
    def radius_outer(self) -> float:
        return self._radius_outer

    @radius_outer.setter
    def radius_outer(self, ro: float):
        if ro <= 0:
            raise ValueError('radius_outer must be positive')

        if ro <= self.radius_inner:
            raise ValueError('radius_outer must be larger than radius_inner')

        self.radius_outer = ro
