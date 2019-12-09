import numpy as _np

from cdpyr.analysis.force_distribution import force_distribution as _algorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ClosedForm(_algorithm.Algorithm):

    def _evaluate(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  structure_matrix: Matrix,
                  wrench: Vector,
                  force_min: Vector,
                  force_max: Vector,
                  **kwargs):
        # if the structure matrix is square, we can just return the straight
        # forward solution to A.T * x = -w
        if structure_matrix.shape[0] == structure_matrix.shape[1]:
            distribution = _np.linalg.solve(structure_matrix, -wrench)
        else:
            # mean force values
            force_mean = 0.5 * (force_max + force_min)
            # and distribution
            distribution = force_mean - _np.linalg.pinv(structure_matrix).dot(
                    wrench + structure_matrix.dot(force_mean))

        return _algorithm.Result(self, pose, distribution, wrench)


__all__ = [
        'ClosedForm',
]
