import numpy as np_

from cdpyr.analysis.forcedistribution import calculator as _forcedistribution
from cdpyr.numpy import linalg
from cdpyr.robot import robot as _robot
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

    # mean force values
    force_mean = 0.5 * (force_max - force_min)

    # calculate value and return it
    return force_mean - np_.linalg.pinv(structurematrix).dot(
        wrench + structurematrix.dot(force_mean))
