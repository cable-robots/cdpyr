from __future__ import annotations

import numpy as _np

from cdpyr.analysis.structure_matrix import structure_matrix as _algorithm
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPattern3R3T(_algorithm.Algorithm):

    def _evaluate(self,
                  pose: _pose.Pose,
                  platform_anchors: Vector,
                  directions: Matrix):
        return _np.vstack((directions,
                           _np.cross(pose.angular.dcm.dot(platform_anchors),
                                     directions,
                                     axis=0)
                           ))

    def _derivative(self,
                    pose: _pose.Pose,
                    platform_anchors: Vector,
                    directions: Matrix) -> _algorithm.Result:
        raise NotImplementedError()


__all__ = [
        'MotionPattern3R3T',
]
