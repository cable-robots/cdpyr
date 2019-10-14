import numpy as np_
from magic_repr import make_repr

from cdpyr.typing import Matrix, Vector


class Homogenous(object):
    _translation: np_.ndarray
    _rotation: np_.ndarray

    def __init__(self,
                 translation: Vector = None,
                 rotation: Matrix = None
                 ):
        self.translation = translation if translation is not None else [0, 0, 0]
        self.rotation = rotation if rotation is not None else np_.eye(3)

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation: Vector):
        translation = np_.asarray(translation)

        if translation.ndim != 1:
            raise ValueError(
                'translation must be a 1-dimensional vector, was {}'.format(
                    translation.ndim))

        if translation.shape != (3,):
            raise ValueError(
                'translation must be a (3,) vector, was {}'.format(
                    translation.shape))

        self._translation = translation

    @translation.deleter
    def translation(self):
        del self._translation

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: Matrix):
        rotation = np_.asarray(rotation)

        if rotation.ndim != 2:
            raise ValueError(
                'rotation must be a 2-dimensional matrix, was {}'.format(
                    rotation.ndim))

        if rotation.shape != (3, 3):
            raise ValueError(
                'rotation must be a (3,3) matrix, was {}'.format(
                    rotation.shape))

        self._rotation = rotation

    @rotation.deleter
    def rotation(self):
        del self._rotation

    @property
    def matrix(self):
        return np_.vstack(
            (
                np_.hstack(
                    (
                        self.rotation,
                        self.translation[:, np_.newaxis]
                    ),
                ),
                np_.hstack(
                    (
                        np_.zeros(3),
                        np_.ones(1)
                    ),
                )
            ),
        )


Homogenous.__repr__ = make_repr(
    'translation',
    'rotation',
)

__all__ = [
    'Homogenous',
]
