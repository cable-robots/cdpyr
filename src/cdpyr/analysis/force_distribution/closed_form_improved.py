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
            def solve_and_reduce(_structure_matrix,
                                 _force_min,
                                 _force_max,
                                 _wrench):
                # solve the closed form for the given distribution
                distribution = self._closed_form(_structure_matrix,
                                                 0.5 * (
                                                     _force_min +
                                                     _force_max),
                                                 _wrench)

                # logical indices where forces are below and above limits
                violated_below: Vector = distribution < _force_min
                violated_above: Vector = distribution > _force_max
                # logical indices where forces limits violated
                violated: Vector = _np.logical_or(violated_below,
                                                  violated_above)
                # logical indices where force limits are valid
                valid: Vector = _np.logical_not(violated)

                # if all forces are valid, return the calculated distribution
                if valid.all():
                    return distribution

                # check if we can continue projecting the cable force onto
                # the wrench or not
                if _structure_matrix.shape[0] == _structure_matrix.shape[1]:
                    raise ArithmeticError('Cannot reduce forces any more')

                # linear index of force to reduce
                reduce = _np.argmax(_np.isclose(distribution, _np.max(
                    _np.abs(distribution[violated]))))
                # logical indices of forces to keep
                keep = _np.ones_like(valid, dtype=_np.bool)
                keep[reduce] = not keep[reduce]

                # determine the invalid force's value i.e., either minimum or
                # maximum force
                if violated_below[reduce]:
                    invalid_force = force_min[reduce]
                else:
                    invalid_force = force_max[reduce]

                # build new force distribution
                new_distribution = _np.zeros_like(distribution)
                new_distribution[reduce] = invalid_force
                new_distribution[keep] = solve_and_reduce(
                    _structure_matrix[:, keep],
                    _force_min[keep],
                    _force_max[keep],
                    _wrench + _structure_matrix[:, reduce] * invalid_force)

                return new_distribution

            distribution = solve_and_reduce(structure_matrix,
                                            force_min,
                                            force_max,
                                            wrench)

        return {
            'pose':   pose,
            'wrench': wrench,
            'forces': distribution,
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

        # no violations?
        if not violated.any():
            # return that force distribution
            return current_force_distribution

        # get logical value where the biggest violation is
        invalid = _np.abs(current_force_distribution) == _np.max(
            _np.abs(current_force_distribution[violated]))
        # and also where the biggest violation is not
        valid = _np.logical_not(invalid)

        # also get the linear index of the invalid force
        idx_invalid = _np.argmax(invalid)

        # determine the invalid force's value i.e., either minimum or maximum
        # force
        if violated_below[idx_invalid]:
            invalid_force = force_min[idx_invalid]
        else:
            invalid_force = force_min[idx_invalid]

        # calculate force distribution for the reduced system
        reduced_force_distribution = self._reduced_iteration(
            current_force_distribution[valid],
            current_structure_matrix[:, valid],
            current_wrench
            + current_structure_matrix[:, idx_invalid] * invalid_force,
            force_min[valid],
            force_max[valid]
        )

        # build new force distribution
        new_force_distribution = _np.zeros_like(current_force_distribution)
        new_force_distribution[valid] = reduced_force_distribution
        new_force_distribution[invalid] = invalid_force

        # and return result
        return new_force_distribution


__all__ = [
    'ClosedFormImproved',
]
