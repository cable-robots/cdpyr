from typing import Optional, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector
from cdpyr.kinematics.transformation import angular as _angular, linear as _linear

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Homogenous(BaseObject):
    linear: '_linear.Linear'
    angular: '_angular.Angular'

    def __init__(self,
                 translation: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None
                 ):
        # init internal variables
        self.linear = _linear.Linear()
        self.angular = _angular.Angular()
        # and set values
        self.translation = translation if translation is not None else [0, 0, 0]
        self.dcm = dcm if dcm is not None else np_.eye(3)

    @property
    def translation(self):
        return self.linear.position

    @translation.setter
    def translation(self, translation: Vector):
        self.linear.position = np_.asarray(translation)

    @translation.deleter
    def translation(self):
        del self.linear

    @property
    def dcm(self):
        return self.angular.dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        self.angular.dcm = np_.asarray(dcm)

    @dcm.deleter
    def dcm(self):
        del self.angular

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
        # deal only with numpy arrays
        coordinates = np_.asarray(coordinates)

        # check if we have a single coordinate
        single = coordinates.ndim == 1

        # ensure coordinates is a 3xM array
        if single:
            coordinates = coordinates[:, np_.newaxis]

        # stack coordinates above a row of `1`
        coordinates = np_.vstack(
            (coordinates, np_.ones(tuple([1]) + coordinates.shape[1:])))

        # First, apply the transformation
        transformed = self.matrix.dot(coordinates)

        # Return whatever we have
        return transformed[0:3,0] if single else transformed[0:3,:]

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
