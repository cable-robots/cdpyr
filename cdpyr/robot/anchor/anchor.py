from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.kinematics.transformation.angular import (
    Angular as AngularTransformation,
    AngularSchema as AngularTransformationSchema,
)
from cdpyr.kinematics.transformation.linear import (
    Linear as LinearTransformation,
    LinearSchema as LinearTransformationSchema,
)
from cdpyr.mixins.lists import DispatcherList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Anchor(object):
    _linear: LinearTransformation
    _angular: AngularTransformation

    def __init__(self,
                 position: Optional[
                     Union[_TVector, LinearTransformation]] = None,
                 rotation: Optional[
                     Union[_TMatrix, AngularTransformation]] = None
                 ):
        # initialize properties
        self.linear = LinearTransformation()
        self.angular = AngularTransformation()

        # set value
        self.position = position or [0, 0, 0]
        self.dcm = rotation or [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    @property
    def position(self):
        return self.linear.position

    @position.setter
    def position(self, position: Union[_TVector, LinearTransformation]):
        if isinstance(position, LinearTransformation):
            position = position.position

        self.linear.position = position

    @position.deleter
    def position(self):
        del self.linear.position

    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, linear: LinearTransformation):
        self._linear = linear

    @linear.deleter
    def linear(self):
        del self.linear

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: AngularTransformation):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self.angular

    @property
    def dcm(self):
        return self.angular.dcm

    @dcm.setter
    def dcm(self, dcm: Union[_TMatrix, AngularTransformation]):
        if isinstance(dcm, AngularTransformation):
            dcm = dcm.dcm
        self.angular.dcm = dcm

    @dcm.deleter
    def dcm(self):
        del self.angular

    @property
    def quaternion(self):
        return self.angular.quaternion

    @quaternion.setter
    def quaternion(self, quaternion: Union[_TVector, AngularTransformation]):
        if isinstance(quaternion, AngularTransformation):
            quaternion = quaternion.quaternion
        self.angular.quaternion = quaternion

    @quaternion.deleter
    def quaternion(self):
        del self.angular

    @property
    def rotvec(self):
        return self.angular.rotvec

    @rotvec.setter
    def rotvec(self, rotvec: Union[_TVector, AngularTransformation]):
        if isinstance(rotvec, AngularTransformation):
            rotvec = rotvec.rotvec
        self.angular.rotvec = rotvec

    @rotvec.deleter
    def rotvec(self):
        del self.angular

    @property
    def euler(self):
        return self.angular.euler

    @euler.setter
    def euler(self, euler: Union[_TVector, AngularTransformation]):
        if isinstance(euler, AngularTransformation):
            euler = euler.euler
        self.angular.euler = euler

    @euler.deleter
    def euler(self):
        del self.angular


Anchor.__repr__ = make_repr(
    'position',
    'dcm'
)


class AnchorSchema(Schema):
    position = fields.Nested(LinearTransformationSchema)
    dcm = fields.Nested(AngularTransformationSchema)

    __model__ = Anchor

    @post_load
    def make_anchor(self, data):
        return self.__model__(**data)


class AnchorList(DispatcherList):

    def __dir__(self):
        return Anchor.__dict__.keys()


__all__ = ['Anchor', 'AnchorList', 'AnchorSchema']
