from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Linear',
]

from typing import Optional, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation import transformation as _transformation
from cdpyr.typing import Matrix, Vector


class Linear(_transformation.Transformation):
    _position: np_.ndarray
    _velocity: np_.ndarray
    _acceleration: np_.ndarray

    def __init__(self,
                 position: Optional[Vector] = None,
                 velocity: Optional[Vector] = None,
                 acceleration: Optional[Vector] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.position = position \
            if position is not None \
            else [0.0, 0.0, 0.0]
        self.velocity = velocity \
            if velocity is not None \
            else [0.0, 0.0, 0.0]
        self.acceleration = acceleration \
            if acceleration is not None \
            else [0.0, 0.0, 0.0]

    @staticmethod
    def random(num: int = None, dim: int = 3):
        """
        Create random linear transformation objects.

        Parameters
        ----------
        num : int
            Number of random linear transformation objects to create.
            Defaults to ``1``.
        dim : int
            Number of random dimensions. Maximum of 3 dimensions can be set, if
            less than 3, the remaining dimensions are set to 0

        Returns
        -------
        obj : Linear
            Returns a single object instance or a generator over ``num``
            objects if ``num > 1``.

        """
        # how many dimensions to pad
        pad_dim = 3 - dim

        # single object
        if num is None or num == 1:
            return Linear(position=np_.pad(2 * (np_.random.random(dim) - 0.5),
                                           (0, pad_dim)))
        else:
            return (Linear(position=pos) for pos in
                    np_.pad(2 * (np_.random.random((num, dim)) - 0.5),
                            (0, pad_dim)))

    def apply(self, coordinates: Union[Vector, Matrix]):
        # deal only with numpy arrays
        coordinates = np_.asarray(coordinates)

        # check if we have a single coordinate
        single = coordinates.ndim == 1

        # return a single transformed coordinate, or all
        return self.position + coordinates if single \
            else self.position[:, None] + coordinates

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector):
        self._position = np_.asarray(position)

    @position.deleter
    def position(self):
        del self._position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Vector):
        self._velocity = np_.asarray(velocity)

    @velocity.deleter
    def velocity(self):
        del self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Vector):
        self._acceleration = np_.asarray(acceleration)

    @acceleration.deleter
    def acceleration(self):
        del self._acceleration

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.position, other.position) \
               and np_.allclose(self.velocity, other.velocity) \
               and np_.allclose(self.acceleration, other.acceleration)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.position < other.position).any() \
               or (self.velocity < other.velocity).any() \
               or (self.acceleration < other.acceleration).any()

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.position <= other.position).any() \
               or (self.velocity <= other.velocity).any() \
               or (self.acceleration <= other.acceleration).any()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.position > other.position).any() \
               or (self.velocity > other.velocity).any() \
               or (self.acceleration > other.acceleration).any()

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.position >= other.position).any() \
               or (self.velocity >= other.velocity).any() \
               or (self.acceleration >= other.acceleration).any()

    def __hash__(self):
        return hash((id(self.acceleration),
                     id(self.position),
                     id(self.velocity)))

    __repr__ = make_repr(
            'position',
            'velocity',
            'acceleration'
    )
