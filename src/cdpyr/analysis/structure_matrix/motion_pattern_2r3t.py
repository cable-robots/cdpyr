from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'MotionPattern2R3T',
]

import numpy as _np

from cdpyr.analysis.structure_matrix import structure_matrix as _algorithm
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector


class MotionPattern2R3T(_algorithm.Algorithm):

    def _evaluate(self,
                  pose: _pose.Pose,
                  platform_anchors: Vector,
                  directions: Matrix):
        return _np.hstack((
                directions,
                pose.angular.dcm.dot(
                        _np.cross(
                                platform_anchors,
                                directions,
                                axis=1).transpose()
                )[0:2, :].transpose())).transpose()

    def _derivative(self,
                    pose: _pose.Pose,
                    platform_anchors: Vector,
                    directions: Matrix) -> _algorithm.Result:
        raise NotImplementedError()
