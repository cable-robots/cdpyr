from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Algorithm',
        'Result',
]

from abc import abstractmethod
from typing import Union

import numpy as _np
from magic_repr import make_repr
from scipy.linalg import null_space

from cdpyr.analysis import evaluator as _evaluator, result as _result
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector


class Algorithm(_evaluator.Evaluator):

    def evaluate(self,
                 pose: _pose.Pose,
                 platform_anchors: Vector,
                 directions: Matrix) -> Result:
        return Result(pose, self._evaluate(pose, platform_anchors, directions))

    def derivative(self,
                   pose: _pose.Pose,
                   platform_anchors: Vector,
                   directions: Matrix) -> Result:
        return self._derivative(pose, platform_anchors, directions)

    @abstractmethod
    def _evaluate(self,
                  pose: _pose.Pose,
                  platform_anchors: Vector,
                  directions: Matrix) -> Result:
        raise NotImplementedError()

    @abstractmethod
    def _derivative(self,
                    pose: _pose.Pose,
                    platform_anchors: Vector,
                    directions: Matrix) -> Result:
        raise NotImplementedError()


class Result(_result.PoseResult):
    _matrix: Matrix
    _kernel: Matrix
    _pinv: Matrix

    def __init__(self,
                 pose: _pose.Pose,
                 matrix: Union[Matrix, Result],
                 **kwargs):
        super().__init__(pose=pose, **kwargs)
        self._matrix = matrix.matrix if isinstance(matrix, Result) else matrix
        self._kernel = None
        self._pinv = None

    @property
    def inv(self):
        return self.pinv

    @property
    def is_singular(self):
        # according to Pott.2018, a pose is singular if the structure
        # matrix's rank is smaller than the number of degrees of freedom
        # i.e., the structure matrix's number of rows
        return _np.linalg.matrix_rank(self._matrix) >= self._matrix.shape[0]

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
        if self._pinv is None:
            if self._matrix.shape[0] == self._matrix.shape[1]:
                self._pinv = _np.linalg.inv(self._matrix)
            else:
                self._pinv = _np.linalg.pinv(self._matrix)

        return self._pinv

    __repr__ = make_repr(
            'pose',
            'matrix',
            'kernel',
    )
