from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'MotionPattern1T',
]

from cdpyr.analysis.structure_matrix import structure_matrix as _algorithm
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector


class MotionPattern1T(_algorithm.Algorithm):

    def _evaluate(self,
                  pose: _pose.Pose,
                  platform_anchors: Vector,
                  directions: Matrix):
        return directions[0:1, :]

    def _derivative(self,
                    pose: _pose.Pose,
                    platform_anchors: Vector,
                    directions: Matrix) -> _algorithm.Result:
        raise NotImplementedError()
