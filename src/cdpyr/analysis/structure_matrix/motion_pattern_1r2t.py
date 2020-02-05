from __future__ import annotations

import numpy as _np

from cdpyr.analysis.structure_matrix import structure_matrix as _algorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPattern1R2T(_algorithm.Algorithm):

    def _evaluate(self,
                  pose: _pose.Pose,
                  platform_anchors: Vector,
                  directions: Matrix):
        return _algorithm.Result(pose, _np.vstack(
                (
                        directions,
                        _np.cross(
                                pose.angular.dcm[0:2, 0:2].dot(
                                        platform_anchors[0:2, :]
                                ),
                                directions[0:2, :],
                                axis=0
                        )
                )
        ),
                                 )


__all__ = [
        'MotionPattern1R2T',
]
