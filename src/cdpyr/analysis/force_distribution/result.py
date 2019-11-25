import copy

from magic_repr import make_repr

from cdpyr.analysis import result as _result
from cdpyr.analysis.force_distribution import algorithm as \
    _force_distribution
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(_result.Result):
    _algorithm: '_force_distribution.Algorithm'
    _forces: Vector
    _wrench: Vector

    def __init__(self,
                 algorithm: '_force_distribution.Algorithm',
                 pose: '_pose.Pose',
                 forces: Vector,
                 wrench: Vector,
                 **kwargs):
        super().__init__(pose)
        self._algorithm = copy.deepcopy(algorithm)
        self._forces = forces
        self._wrench = wrench

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def forces(self):
        return self._forces

    @property
    def wrench(self):
        return self._wrench

    __repr__ = make_repr(
        'algorithm',
        'pose',
        'distribution',
    )


__all__ = [
    'Result',
]
