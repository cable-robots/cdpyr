import numpy as np_
import scipy

from cdpyr.analysis.forcedistribution.algorithm.algorithminterface import \
    AlgorithmInterface as ForceDistributionAlgorithmInterface
from cdpyr.numpy import linalg
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ClosedForm(ForceDistributionAlgorithmInterface):

    @classmethod
    def calculate(cls,
                  robot: '_robot.Robot',
                  structurematrix: Matrix,
                  wrench: Vector,
                  **kwargs):
        # validate structure matrix has at least as many columns as rows
        if structurematrix.shape[1] < structurematrix.shape[0]:
            raise ValueError(
                'Expected structure matrix to be at least quadratic or have '
                'more columns than rows')

        # if the structure matrix is square, we can just return the straight
        # forward solution to A.T * x = -w
        if linalg.issquare(structurematrix):
            return scipy.linalg.solve(structurematrix, -wrench)

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

        # calculate value and return it
        return force_mean - np_.linalg.pinv(structurematrix).dot(
            wrench + structurematrix.dot(force_mean))
