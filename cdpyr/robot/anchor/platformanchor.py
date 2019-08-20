from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.kinematics.transformation.angular import \
    Angular as AngularTransformation
from cdpyr.kinematics.transformation.linear import Linear as \
    LinearTransformation
from cdpyr.robot.anchor.anchor import Anchor, AnchorList, AnchorSchema

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class PlatformAnchor(Anchor):

    def __init__(self,
                 position: Optional[
                     Union[_TVector, LinearTransformation]] = None,
                 rotation: Optional[
                     Union[_TMatrix, AngularTransformation]] = None):
        """ Generic anchor type that is attached to the platform.

        :param Union[_TVector, LinearTransformation] position: Optional
        position of the platform anchor given either as (3,) numpy array or
        a 3-element list. Coordinates are assumed given with respect to the
        platform's coordinate system and in SI units [ m ] (meter)
        :param Union[_TMatrix, AngularTransformation] rotation: Optional
        orientation of the platform anchor given as (3,3) numpy array (a DCM)
        or a 3-element list of 3-element lists.
        """
        Anchor.__init__(self, position=position, rotation=rotation)


PlatformAnchor.__repr__ = make_repr(
    'position',
    'dcm'
)


class PlatformAnchorSchema(AnchorSchema):
    __model__ = PlatformAnchor


class PlatformAnchorList(AnchorList):

    def __dir__(self):
        return PlatformAnchor.__dict__.keys()


__all__ = ['PlatformAnchor', 'PlatformAnchorList', 'PlatformAnchorSchema']
