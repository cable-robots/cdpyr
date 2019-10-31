import numpy as _np

from cdpyr.analysis.structure_matrix import algorithm as _algorithm
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__copyright__ = "Copyright 2019, Philipp Tempel"
__license__ = "EUPL v1.2"


class MotionPattern2R3T(_algorithm.Algorithm):
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
                    )[0:2, :]
                )
            ),
        }


__all__ = [
    'MotionPattern2R3T',
]
