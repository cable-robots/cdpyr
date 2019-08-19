from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class StandardKinematics(object):

    def forward(self,
                robot: Robot,
                pose: Pose
                ):
        raise NotImplementedError

    def backward(self,
                 robot: Robot,
                 pose: Pose
                 ):
        raise NotImplementedError


StandardKinematics.__repr__ = make_repr()

__all__ = ['StandardKinematics']
