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
        return _algorithm.Result(pose, _np.vstack(
                (
                        directions,
                        _np.cross(
                                pose.angular.dcm.dot(
                                        platform_anchors
                                ),
                                directions,
                                axis=0
                        )[0:2, :]
                )
        ),
                                 )
