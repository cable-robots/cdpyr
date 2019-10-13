import numpy as np_

from cdpyr.analysis.forcedistribution.algorithm.algorithminterface import \
    AlgorithmInterface as ForceDistributionAlgorithm
from cdpyr.numpy import linalg
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ClosedForm(ForceDistributionAlgorithm):

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

        # calculate value and return it
        return force_mean - np_.linalg.pinv(structurematrix).dot(
            wrench + structurematrix.dot(force_mean))
