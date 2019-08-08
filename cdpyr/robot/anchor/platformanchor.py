from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mechanics.transformation.angular import \
    Angular as AngularTransformation
from cdpyr.mechanics.transformation.linear import Linear as LinearTransformation
from cdpyr.robot.anchor.anchor import Anchor
from cdpyr.robot.anchor.anchor import AnchorList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class PlatformAnchor(Anchor):

    def __init__(self,
                 position: Optional[
                     Union[_TVector, LinearTransformation]] = None,
                 rotation: Optional[
                     Union[_TMatrix, AngularTransformation]] = None):
        Anchor.__init__(self, position=position, rotation=rotation)


PlatformAnchor.__repr__ = make_repr(
    'position',
    'dcm'
)


class PlatformAnchorList(AnchorList):

    def __dir__(self):
        return PlatformAnchor.__dict__.keys()


__all__ = ['PlatformAnchor', 'PlatformAnchorList']
