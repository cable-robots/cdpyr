import numpy as _np

from cdpyr.analysis.structure_matrix.structure_matrix import Algorithm as \
    StructureMatrixAlgorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPattern2R3T(StructureMatrixAlgorithm):

    def _evaluate(self,
                  platform_anchors: Vector,
                  pose: '_pose.Pose',
                  directions: Matrix):
        return {
                'matrix': _np.vstack(
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
        }


__all__ = [
        'MotionPattern2R3T',
]
