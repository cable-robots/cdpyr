import numpy as _np
from magic_repr import make_repr
from scipy.linalg import null_space

from cdpyr.analysis import result as _result
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__copyright__ = "Copyright 2019, Philipp Tempel"
__license__ = "EUPL v1.2"


class Result(_result.Result):
    _matrix: Matrix
    _kernel: Matrix

    def __init__(self, pose: '_pose.Pose', matrix: Matrix):
        super().__init__(pose)
        self._matrix = matrix
        self._kernel = None

    @property
    def inv(self):
        if self._matrix.shape[0] != self._matrix.shape[1]:
            return self.pinv

        return _np.linalg.inv(self._matrix)

    @property
    def is_singular(self):
        return _np.linalg.matrix_rank(self.matrix) >= self.matrix.shape[0]

    @property
    def kernel(self):
        if self._kernel is None:
            self._kernel = null_space(self._matrix)

        return self._kernel

    @property
    def matrix(self):
        return self._matrix

    @property
    def null_space(self):
        return self.kernel

    @property
    def nullspace(self):
        return self.kernel

    @property
    def pinv(self):
        return _np.linalg.pinv(self._matrix)


Result.__repr__ = make_repr(
    'pose',
    'matrix',
    'kernel',
)

__all__ = [
    'Result',
]
