from typing import Optional, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Homogenous(BaseObject):
    _translation: np_.ndarray
    _dcm: np_.ndarray

    def __init__(self,
                 translation: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None
                 ):
        self.translation = translation if translation is not None else [0, 0, 0]
        self.dcm = dcm if dcm is not None else np_.eye(3)

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation: Vector):
        translation = np_.asarray(translation)

        _validator.linalg.space_coordinate(translation, 'translation')

        self._translation = translation

    @translation.deleter
    def translation(self):
        del self._translation

    @property
    def dcm(self):
        return self._dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        dcm = np_.asarray(dcm)

        _validator.linalg.rotation_matrix(dcm, 'dcm')

        self._dcm = dcm

    @dcm.deleter
    def dcm(self):
        del self._dcm

    @property
    def matrix(self):
        return np_.vstack(
            (
                np_.hstack(
                    (
                        self.dcm,
                        self.translation[:, np_.newaxis]
                    ),
                ),
                np_.hstack(
                    (
                        np_.zeros((3,)),
                        1
                    ),
                )
            ),
        )

    def apply(self, coordinates: Union[Vector, Matrix]):
        coordinates = np_.asarray(coordinates)
        # ensure coordinates is a 3xM array
        if coordinates.ndim == 1:
            coordinates = coordinates[:, np_.newaxis]

        # stack coordinates above a row of `1`
        coordinates = np_.vstack(
            (coordinates, np_.ones(tuple([1]) + coordinates.shape[1:])))

        try:
            return np_.stack([self.matrix.dot(page)[0:3, :] for page in
                              np_.rollaxis(coordinates, axis=2)], axis=2)
        except ValueError:
            return self.matrix.dot(coordinates)[0:3, :]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.translation, other.translation) \
               and np_.allclose(self.dcm, other.dcm)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((id(self.dcm), id(self.translation)))

    __repr__ = make_repr(
        'translation',
        'dcm',
    )


__all__ = [
    'Homogenous',
]
