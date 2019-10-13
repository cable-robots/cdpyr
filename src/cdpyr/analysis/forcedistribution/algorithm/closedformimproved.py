import numpy as np_

from cdpyr.analysis.forcedistribution.algorithm.algorithminterface import \
    AlgorithmInterface as ForceDistributionAlgorithm
from cdpyr.numpy import linalg
from cdpyr.typing import Matrix, Vector


class ClosedFormImproved(ForceDistributionAlgorithm):

    @classmethod
    def evaluate(cls,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        # if the structure matrix is square, we can just return the straight
        # forward solution to A.T * x = -w
        if linalg.issquare(structurematrix):
            return np_.linalg.solve(structurematrix, -wrench)

        # get number of cables/forces from the number of columns of the
        # structure matrix
        num_cables = structurematrix.shape[1]

        # parse cable the force limits to be vectors of correct size
        force_min, force_max = cls._parse_force_limits(
            num_cables,
            kwargs.get('force_min', 0),
            kwargs.get('force_max', np_.inf)
        )

        # mean force values
        force_mean = 0.5 * (force_max - force_min)

        # Initial solving of the force distribution
        force_distribution = cls._closed_form(structurematrix,
                                              force_mean,
                                              wrench)

        # And iterate
        try:
            force_distribution = cls._reduced_iteration(
                force_distribution,
                structurematrix,
                wrench,
                force_min,
                force_max
            )
        except ArithmeticError as arrexc:
            raise ValueError(
                'Could not find a valid force distribution using the current '
                'algorithm. Please check your arguments or try another '
                'algorithm if you are sure there must be a valid force '
                'distribution.') from arrexc
        else:
            return force_distribution

    @classmethod
    def _closed_form(cls,
                     structurematrix: Matrix,
                     force_mean: Vector,
                     wrench: Vector):
        # return a quick form of the closed form
        return force_mean - np_.linalg.pinv(structurematrix).dot(
            wrench + structurematrix.dot(force_mean))

    @classmethod
    def _reduced_iteration(cls,
                           current_force_distribution: Vector,
                           current_structure_matrix: Matrix,
                           current_wrench: Vector,
                           force_min: Vector,
                           force_max: Vector
                           ):
        # find where force limits are violated
        violated_below: Vector = current_force_distribution < force_min
        violated_above: Vector = force_max < current_force_distribution
        violated: Vector = np_.logical_xor(violated_below, violated_above)
        valid: Vector = np_.invert(violated)

        # also get the linear indices of the violations (needed for later
        # proper re-concatenation of full force vector)
        idx_violated_below: Vector = np_.where(violated_below)[0]
        idx_violated_above: Vector = np_.where(violated_above)[0]
        idx_violated: Vector = np_.where(violated)[0]
        idx_valid: Vector = np_.where(valid)[0]
        num_violations = idx_violated.size

        # if there are no violations, bail out right away
        if 0 == num_violations:
            return current_force_distribution

        # if there are any violations, we need to check to see if we can
        # reduce the structure matrix by the amount of violations
        if current_structure_matrix.shape[1] - num_violations > \
            current_structure_matrix.shape[0]:
            raise ArithmeticError(
                'Unable to reduce structure matrix further. Expected it to be '
                '({}, {}), but was {}.'.format(
                    current_structure_matrix.shape[0],
                    current_structure_matrix.shape[0]
                    + idx_violated_below.size
                    + idx_violated_below.size,
                    current_structure_matrix.shape
                ))

        # calculate force distribution for the reduced system
        reduced_force_distribution = cls._reduced_iteration(
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
        new_force_distribution = np_.zeros_like(current_force_distribution)
        new_force_distribution[violated_below] = force_min[violated_below]
        new_force_distribution[violated_above] = force_max[violated_above]
        new_force_distribution[valid] = reduced_force_distribution

        # and return result
        return new_force_distribution
