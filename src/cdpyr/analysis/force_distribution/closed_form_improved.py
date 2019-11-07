import numpy as _np

from cdpyr.analysis.force_distribution import (
    algorithm as _algorithm,
)
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ClosedFormImproved(_algorithm.Algorithm):

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
        # non-square structure matrix case
        else:
            # mean force values
            force_mean = 0.5 * (force_max - force_min)

            # Initial solving of the force distribution
            distribution = self._closed_form(structure_matrix,
                                             force_mean,
                                             wrench)

            # And iterate
            try:
                distribution = self._reduced_iteration(
                    distribution,
                    structure_matrix,
                    wrench,
                    force_min,
                    force_max
                )

                if (distribution == _np.nan).any():
                    raise ArithmeticError(
                        'Calculation yielded NaN values in the force '
                        'distribution.')
            except ArithmeticError as ArithmeticE:
                raise ValueError(
                    'Could not find a valid force distribution using the '
                    'current algorithm_old. Please check your arguments or '
                    'try another algorithm_old if you are sure there must be '
                    'a valid force distribution.') \
                    from ArithmeticE

        return {
            'pose':         pose,
            'wrench':       wrench,
            'distribution': distribution,
        }

    def _closed_form(self,
                     structure_matrix: Matrix,
                     force_mean: Vector,
                     wrench: Vector):
        # return a quick form of the closed form
        return force_mean - _np.linalg.pinv(structure_matrix).dot(
            wrench + structure_matrix.dot(force_mean))

    def _reduced_iteration(self,
                           current_force_distribution: Vector,
                           current_structure_matrix: Matrix,
                           current_wrench: Vector,
                           force_min: Vector,
                           force_max: Vector
                           ):
        # find where force limits are violated
        violated_below: Vector = current_force_distribution < force_min
        violated_above: Vector = force_max < current_force_distribution
        violated: Vector = _np.logical_xor(violated_below, violated_above)
        valid: Vector = _np.invert(violated)

        # also get the linear indices of the violations (needed for later
        # proper re-concatenation of full force vector)
        # idx_violated_below: Vector = np_.where(violated_below)[0]
        # idx_violated_above: Vector = np_.where(violated_above)[0]
        idx_violated: Vector = _np.where(violated)[0]
        # idx_valid: Vector = np_.where(valid)[0]
        num_violations = idx_violated.size

        # if there are no violations, bail out right away
        if 0 == num_violations:
            return current_force_distribution

        # if there are any violations, we need to check to see if we can
        # reduce the structure matrix by the amount of violations
        if num_violations > current_structure_matrix.shape[1] - \
            current_structure_matrix.shape[0]:
            raise ArithmeticError(
                'Unable to reduce structure matrix further. Expected it to be '
                '({}, {}), but was {}.'.format(
                    current_structure_matrix.shape[0],
                    current_structure_matrix.shape[0]
                    + num_violations,
                    current_structure_matrix.shape
                ))

        # calculate force distribution for the reduced system
        reduced_force_distribution = self._reduced_iteration(
            current_force_distribution[valid],
            current_structure_matrix[:, valid],
            current_wrench
            + current_structure_matrix[:, violated_below].dot(
                force_min[violated_below]
            )
            + current_structure_matrix[:, violated_above].dot(
                force_min[violated_above]
            ),
            force_min[valid],
            force_max[valid]
        )

        # build new force distribution
        new_force_distribution = _np.zeros_like(current_force_distribution)
        new_force_distribution[violated_below] = force_min[violated_below]
        new_force_distribution[violated_above] = force_max[violated_above]
        new_force_distribution[valid] = reduced_force_distribution

        # and return result
        return new_force_distribution


__all__ = [
    'ClosedFormImproved',
]
