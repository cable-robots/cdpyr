from collections import UserList
from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from .pose import Pose

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class PoseList(UserList):
    data: Sequence[Pose]

    def __init__(self, poses: None):
        super().__init__(self)
        self.data = poses or []

    @property
    def poses(self):
        return self.data

    @poses.setter
    def poses(self, poses: Sequence[Pose]):
        self.data = poses

    @poses.deleter
    def poses(self):
        del self.data


PoseList.__repr__ = make_repr(
    'poses'
)
