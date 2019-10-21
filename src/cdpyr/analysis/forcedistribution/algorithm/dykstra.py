import numpy as np_

from cdpyr import validator as _validator
from cdpyr.analysis.forcedistribution import calculator as _forcedistribution
from cdpyr.numpy import linalg
from cdpyr.typing import Matrix, Vector


def evaluate(calculator: '_forcedistribution.Calculator',
             structurematrix: Matrix,
             wrench: Vector,
             force_min: Vector,
             force_max: Vector,
             **kwargs):
    # if the structure matrix is square, we can just return the straight
    # forward solution to A.T * x = -w
    if linalg.issquare(structurematrix):
        return np_.linalg.solve(structurematrix, -wrench)

    # number of maximum iterations
    max_iter = kwargs.get('maxiter', 5000)
    _validator.numeric.greater_than(max_iter, 0, 'max_iter')
    # threshold for projection
    eps_projection = kwargs.get('eps_projection', 1e-3)
    _validator.numeric.greater_than(eps_projection, 0, 'eps_projection')
    _validator.numeric.less_than(eps_projection, 1, 'eps_projection')
    # threshold for convergence
    eps_convergence = kwargs.get('eps_convergence', 1e-6)
    _validator.numeric.greater_than(eps_convergence, 0, 'eps_convergence')
    _validator.numeric.less_than(eps_convergence, 1, 'eps_convergence')

    # get number of cables/forces from the number of columns of the
    # structure matrix
    num_cables = structurematrix.shape[1]

    # initialize loop variables
    converged = False
    kiter = 1
    eye = np_.eye(num_cables)

    # pseude-inverse of structure matrix
    structurematrix_pinv = np_.linalg.pinv(structurematrix)

    # initial projection before loop starts
    projection_c = projection_a = 0.5 * (force_min + force_max) * np_.ones(
        num_cables)

    # actual loop
    while not converged:
        # first projection step
        projection_a_new = (
                               eye
                               - structurematrix_pinv.dot(structurematrix)
                           ).dot(projection_c) \
                           - structurematrix_pinv.dot(wrench)

        # project down onto force limit boundaries
        projection_c_new = np_.minimum(
            np_.maximum(projection_c, force_min),
            force_max
        )

        # check for break conditions
        if np_.linalg.norm(projection_c_new - projection_c,
                           np_.inf) < eps_convergence:
            converged = True
        elif np_.linalg.norm(projection_a_new - projection_a,
                             np_.inf) < eps_convergence:
            converged = True
        elif np_.linalg.norm(projection_a_new - projection_c_new,
                             np_.inf) < eps_projection:
            converged = True

        # iteration update
        projection_a = projection_a_new
        projection_c = projection_c_new

        # and finally increase iteration counter
        kiter += 1

        # fail if not converged
        if kiter >= max_iter:
            raise ArithmeticError(
                'Could not find a valid force distribution using the current '
                'current algorithm. Please check your arguments or try '
                'another algorithm if you are sure there must be a valid '
                'force distribution.')

    return projection_a
