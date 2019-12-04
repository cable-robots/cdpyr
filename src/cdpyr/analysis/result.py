import copy
from abc import ABC

from magic_repr import make_repr

from cdpyr.motion.pose import pose as _pose

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):

    def __init__(self, **kwargs):
        pass


class PlottableResult(Result):
    pass


class PoseResult(Result):
    _pose: '_pose.Pose'

    def __init__(self, pose: '_pose.Pose', **kwargs):
        super().__init__(**kwargs)
        self._pose = copy.deepcopy(pose)

    @property
    def pose(self):
        return self._pose

    __repr__ = make_repr(
            'pose'
    )


__all__ = [
        'PlottableResult',
        'PoseResult',
        'Result',
]
