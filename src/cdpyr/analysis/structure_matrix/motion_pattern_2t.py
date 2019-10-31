from cdpyr.analysis.structure_matrix import algorithm as _algorithm
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPattern2T(_algorithm.Algorithm):
    def evaluate(self,
                 platform: '_platform.Platform',
                 pose: '_pose.Pose',
                 directions: Matrix):
        return {
            'pose':   pose,
            'matrix': directions[0:2, :],
        }


__all__ = [
    'MotionPattern2T',
]
