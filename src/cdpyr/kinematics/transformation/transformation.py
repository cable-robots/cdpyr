from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Transformation',
]

from abc import abstractmethod
from typing import Union

from cdpyr.base import Object
from cdpyr.typing import Matrix, Vector


class Transformation(Object):
    """
    Abstract transformation interface
    """

    @abstractmethod
    def apply(self, coordinates: Union[Vector, Matrix]):
        """
        Abstract method to implement by a concrete transformation type

        A transformation object must support being applied to both vectors
        and matrices and return a matching type (vector and matrix,
        respectively).

        Parameters
        ----------
        coordinates : Union[Vector, Matrix]
            (N,) or (N,M) array of values to apply transformation on. Number
            of dimensions `N` of the coordinates must match the number of
            dimensions the transformation supports and the number of
            coordinates `M` can be more than one to apply transformation to
            any column of `coordinates`.
            The underlying transformation basically performs :code:`A.dot(c)`
            where `A` is the transformation matrix and ```c``` is the vector or
            matrix of coordinates to transform.

        Returns
        -------
        coordinates : Union[Vector, Matrix]
            (N,) or (N,M) vector or matrix of transformed coordinates
            depending on the type of input (vector or matrix).

        """
        raise NotImplementedError()
