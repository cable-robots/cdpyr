from collections import UserList
from typing import Optional, Sequence

from abc import ABC
from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)
from cdpyr.typing import Matrix, Vector


class Anchor(object):
    _linear: '_linear.Linear'
    _angular: '_angular.Angular'

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 linear: Optional['_linear.Linear'] = None,
                 angular: Optional['_angular.Angular'] = None,
                 ):
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
        # initialize and set linear property if not given by the user
        if linear is None:
            self.linear = _linear.Linear()
            self.position = position or [0.0, 0.0, 0.0]
        # set linear transformation to user-defined value
        else:
            self.linear = linear

        # initialize and set angularlinear property if not given by the user
        if angular is None:
            self.angular = _angular.Angular(
                dcm=dcm if dcm is not None else np_.eye(3))
        # set angular transformation to user-defined value
        else:
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
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, linear: '_linear.Linear'):
        self._linear = linear

    @linear.deleter
    def linear(self):
        del self.linear

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: '_angular.Angular'):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self.angular

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


Anchor.__repr__ = make_repr(
    'position',
    'dcm',
    'quaternion',
    'rotvec'
)


class AnchorList(UserList, ABC):
    data: Sequence[Anchor]

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


__all__ = [
    'Anchor',
    'AnchorList',
]
