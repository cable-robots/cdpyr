from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'ClosedFormImproved',
]

import numpy as _np

from cdpyr.analysis.force_distribution import force_distribution as _algorithm
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ClosedFormImproved(_algorithm.Algorithm):

    def _evaluate(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
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
                    raise ArithmeticError('Cannot reduce forces any more.')

                # calculate the amount of violation
                violated_amount = _np.zeros_like(distribution)
                if violated_below.any():
                    violated_amount[violated_below] = _force_min[
                                                          violated_below] - \
                                                      distribution[
                                                          violated_below]
                if violated_above.any():
                    violated_amount[violated_above] = distribution[
                                                          violated_above] - \
                                                      _force_max[violated_above]

                # linear index of force to reduce
                reduce = _np.argmax(_np.abs(violated_amount))
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

        return _algorithm.Result(self, pose, distribution, wrench)

    def _closed_form(self,
                     structure_matrix: Matrix,
                     force_mean: Vector,
                     wrench: Vector):
        # return a quick form of the closed form
        return force_mean - _np.linalg.pinv(structure_matrix).dot(
                wrench + structure_matrix.dot(force_mean))
