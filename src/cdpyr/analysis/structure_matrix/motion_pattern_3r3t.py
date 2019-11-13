import numpy as _np

from cdpyr.analysis.structure_matrix import algorithm as _algorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPattern3R3T(_algorithm.Algorithm):
    def evaluate(self,
                 platform: '_platform.Platform',
                 pose: '_pose.Pose',
                 directions: Matrix):
        return {
            'pose':   pose,
            'matrix': _np.vstack(
                (
                    directions,
                    _np.cross(
                        pose.angular.dcm.dot(
                            platform.bi
                        ),
                        directions,
                        axis=0
                    )
                )
            ),
        }


__all__ = [
    'MotionPattern3R3T',
]
