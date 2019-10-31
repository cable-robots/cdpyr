from typing import Union

import numpy as _np

from cdpyr import validator as _validator
from cdpyr.analysis.force_distribution import (
    algorithm as _algorithm,
)
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Dykstra(_algorithm.Algorithm):
    _maximum_iterations: int
    _threshold_projection: float
    _threshold_convergence: float

    def __init__(self, kinematics: '_kinematics.Algorithm',
                 force_minimum: Union[Num, Vector],
                 force_maximum: Union[Num, Vector],
                 max_iterations: int = 5000,
                 eps_projection: float = 1e-3,
                 eps_convergence: float = 1e-6):
        super().__init__(kinematics, force_minimum, force_maximum)
        self.maximum_iterations = max_iterations
        self.threshold_projection = eps_projection
        self.threshold_convergence = eps_convergence

    @property
    def maximum_iterations(self):
        return self._maximum_iterations

    @maximum_iterations.setter
    def maximum_iterations(self, iterations: int):
        _validator.numeric.greater_than_or_equal_to(iterations,
                                                    1,
                                                    'maximum_iterations')
        self._maximum_iterations = iterations

    @maximum_iterations.deleter
    def maximum_iterations(self):
        del self._maximum_iterations

    @property
    def threshold_projection(self):
        return self._threshold_projection

    @threshold_projection.setter
    def threshold_projection(self, threshold: float):
        _validator.numeric.less_than_or_equal_to(threshold,
                                                 1,
                                                 'threshold_projection')
        _validator.numeric.greater_than(threshold,
                                        0,
                                        'threshold_projection')

        self._threshold_projection = threshold

    @threshold_projection.deleter
    def threshold_projection(self):
        del self._threshold_projection

    @property
    def threshold_convergence(self):
        return self._threshold_convergence

    @threshold_convergence.setter
    def threshold_convergence(self, threshold: float):
        _validator.numeric.less_than_or_equal_to(threshold,
                                                 1,
                                                 'threshold_convergence')
        _validator.numeric.greater_than(threshold,
                                        0,
                                        'threshold_convergence')

        self._threshold_convergence = threshold

    @threshold_convergence.deleter
    def threshold_convergence(self):
        del self._threshold_convergence

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
        # non-square structure matrix
        else:
            # number of maximum iterations
            max_iter = self.maximum_iterations
            # threshold for projection
            eps_projection = self.threshold_projection
            # threshold for convergence
            eps_convergence = self.threshold_convergence

            # get number of cables/forces from the number of columns of the
            # structure matrix
            num_cables = robot.num_kinematic_chains

            # initialize loop variables
            converged = False
            kiter = 1
            eye = _np.eye(num_cables)

            # pseude-inverse of structure matrix
            structurematrix_pinv = _np.linalg.pinv(structure_matrix)

            # initial projection before loop starts
            projection_c = projection_a = 0.5 * (
                force_min + force_max) * _np.ones(
                num_cables)

            # actual loop
            while not converged:
                # first projection step
                projection_a_new = (
                                       eye
                                       - structurematrix_pinv.dot(
                                       structure_matrix)
                                   ).dot(projection_c) \
                                   - structurematrix_pinv.dot(wrench)

                # project down onto force limit boundaries
                projection_c_new = _np.minimum(
                    _np.maximum(projection_c, force_min),
                    force_max
                )

                # check for break conditions
                if _np.linalg.norm(projection_c_new - projection_c,
                                   _np.inf) < eps_convergence:
                    converged = True
                elif _np.linalg.norm(projection_a_new - projection_a,
                                     _np.inf) < eps_convergence:
                    converged = True
                elif _np.linalg.norm(projection_a_new - projection_c_new,
                                     _np.inf) < eps_projection:
                    converged = True

                # iteration update
                projection_a = projection_a_new
                projection_c = projection_c_new

                # and finally increase iteration counter
                kiter += 1

                # fail if not converged
                if kiter >= max_iter:
                    raise ArithmeticError(
                        'Could not find a valid force distribution using the '
                        'current algorithm. Please check your arguments or '
                        'try another algorithm if you are sure there must be '
                        'a valid force distribution.')

                distribution = projection_a

        return {
            'pose':         pose,
            'wrench':       wrench,
            'distribution': distribution,
        }


__all__ = [
    'Dykstra',
]
