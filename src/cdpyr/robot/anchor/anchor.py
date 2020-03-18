from __future__ import annotations

from collections import UserList
from typing import List, Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear
)
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Anchor(RobotComponent):
    linear: _linear.Linear
    angular: _angular.Angular

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 linear: Optional[_linear.Linear] = None,
                 angular: Optional[_angular.Angular] = None,
                 **kwargs):
        """

        Parameters
        ----------
        position : Vector
            (3,) vector of the (relative) position of the anchor in a
            reference coordinate system
        dcm : Matrix
            (3,3) matrix representing the rotation matrix `dcm` of the
            platform anchor. Use only where applicable.
        linear : Linear
            Linear transformation object that is to be used instead of
            `position`  if given.
        angular : Angular
            Angular transformation object that is to be used instead of
            `rotation` if given.
        """
        super().__init__(**kwargs)

        # initialize and set linear property if not given by the user
        if linear is None:
            linear = _linear.Linear(
                    position if position is not None else [0.0, 0.0, 0.0])

        # set linear transformation to inferred value
        self.linear = linear

        # initialize and set angularlinear property if not given by the user
        if angular is None:
            angular = _angular.Angular(
                    dcm=dcm if dcm is not None else np_.eye(3))

        # set linear transformation to inferred value
        self.angular = angular

    @property
    def position(self):
        return self.linear.position

    @position.setter
    def position(self, position: Vector):
        self.linear.position = position

    @position.deleter
    def position(self):
        del self.linear.position

    @property
    def dcm(self):
        return self.angular.dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        self.angular.dcm = dcm

    @dcm.deleter
    def dcm(self):
        del self.angular

    @property
    def quaternion(self):
        return self.angular.quaternion

    @quaternion.setter
    def quaternion(self, quaternion: Vector):
        self.angular.quaternion = quaternion

    @quaternion.deleter
    def quaternion(self):
        del self.angular

    @property
    def rotvec(self):
        return self.angular.rotvec

    @rotvec.setter
    def rotvec(self, rotvec: Vector):
        self.angular.rotvec = rotvec

    @rotvec.deleter
    def rotvec(self):
        del self.angular

    @property
    def euler(self):
        return self.angular.euler

    @euler.setter
    def euler(self, euler: Vector):
        self.angular.euler = euler

    @euler.deleter
    def euler(self):
        del self.angular

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.linear == other.linear \
               and self.angular == other.angular

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.angular, self.linear))

    __repr__ = make_repr(
            'position',
            'dcm',
            'quaternion',
            'rotvec'
    )


class AnchorList(UserList, RobotComponent):
    data: List[Anchor]

    @property
    def angular(self):
        return (anchor.angular for anchor in self.data)

    @property
    def dcm(self):
        return (anchor.dcm for anchor in self.data)

    @property
    def euler(self):
        return (anchor.euler for anchor in self.data)

    @property
    def linear(self):
        return (anchor.linear for anchor in self.data)

    @property
    def position(self):
        return (anchor.position for anchor in self.data)

    @property
    def quaternion(self):
        return (anchor.quaternion for anchor in self.data)

    @property
    def rotvec(self):
        return (anchor.rotvec for anchor in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.data))


__all__ = [
        'Anchor',
        'AnchorList',
]
