from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mechanics.transformation.angular import \
    Angular as AngularTransformation
from cdpyr.mechanics.transformation.linear import Linear as LinearTransformation
from cdpyr.robot.anchor.anchor import Anchor
from cdpyr.robot.anchor.anchor import AnchorList
from cdpyr.robot.drivetrain import DriveTrain
from cdpyr.robot.pulley import Pulley

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class FrameAnchor(Anchor):
    _pulley: Pulley
    _drivetrain: DriveTrain

    def __init__(self,
                 position: Optional[
                     Union[_TVector, LinearTransformation]] = None,
                 rotation: Optional[
                     Union[_TMatrix, AngularTransformation]] = None,
                 pulley: Optional[Pulley] = None,
                 drivetrain: Optional[DriveTrain] = None
                 ):
        Anchor.__init__(self, position=position, rotation=rotation)
        self.pulley = pulley or None
        self.drivetrain = drivetrain or None

    @property
    def pulley(self):
        return self._pulley

    @pulley.setter
    def pulley(self, pulley: Pulley):
        self._pulley = pulley

    @pulley.deleter
    def pulley(self):
        del self._pulley

    @property
    def drivetrain(self):
        return self._drivetrain

    @drivetrain.setter
    def drivetrain(self, drivetrain: DriveTrain):
        self._drivetrain = drivetrain

    @drivetrain.deleter
    def drivetrain(self):
        del self._drivetrain


FrameAnchor.__repr__ = make_repr(
    'position',
    'dcm',
    'pulley',
    'drivetrain'
)


class FrameAnchorList(AnchorList):

    def __dir__(self):
        return FrameAnchor.__dict__.keys()


__all__ = ['FrameAnchor', 'FrameAnchorList']
