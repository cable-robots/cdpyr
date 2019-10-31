import copy
from abc import ABC
from magic_repr import make_repr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):
    _pose: object

    def __init__(self, pose):
        self._pose = copy.deepcopy(pose)

    @property
    def pose(self):
        return self._pose


Result.__repr__ = make_repr(
    'pose'
)

__all__ = [
    'Result',
]
