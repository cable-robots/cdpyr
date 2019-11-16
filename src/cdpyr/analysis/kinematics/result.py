import copy
from magic_repr import make_repr

from cdpyr.analysis import result as _result
from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(_result.Result):
    _algorithm: '_kinematics.Algorithm'
    _directions: Matrix
    _joints: Vector
    _swivel: Vector
    _wrap: Vector

    def __init__(self,
                 algorithm: '_kinematics.Algorithm',
                 pose: '_pose.Pose',
                 joints: Vector,
                 directions: Matrix,
                 swivel: Vector = None,
                 wrap: Vector = None,
                 **kwargs):
        super().__init__(pose)
        self._algorithm = copy.deepcopy(algorithm)
        self._joints = joints
        self._directions = directions
        self._swivel = swivel
        self._wrap = wrap

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def cable_lengths(self):
        return self.joints

    @property
    def directions(self):
        return self._directions

    @property
    def joints(self):
        return self._joints

    @property
    def lengths(self):
        return self._joints

    @property
    def swivel(self):
        return self._swivel

    @property
    def wrap(self):
        return self._wrap

    __repr__ = make_repr(
        'algorithm',
        'pose',
        'joints',
        'swivel',
        'wrap',
    )


__all__ = [
    'Result',
]
