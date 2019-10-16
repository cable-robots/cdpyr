import numpy as np_
from enum import Enum

from cdpyr.analysis.forcedistribution import algorithm as _algorithm
from cdpyr.analysis.forcedistribution.algorithm.algorithminterface import \
    AlgorithmInterface as ForceDistributionAlgorithm
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ForceDistribution(Enum):
    CLOSED_FORM = _algorithm.ClosedForm
    CLOSED_FORM_IMPROVED = _algorithm.ClosedFormImproved
    DYKSTRA = _algorithm.Dykstra

    @property
    def algorithm(self) -> ForceDistributionAlgorithm:
        return self._value_

    def evaluate(self,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        # validate structure matrix has at least as many columns as rows
        if structurematrix.shape[1] < structurematrix.shape[0]:
            raise ValueError(
                'Expected structure to be at least ({}, {}) but received {'
                '}.'.format(
                    wrench.shape[1],
                    wrench.shape[1],
                    structurematrix.shape
                ))

        return self.algorithm.evaluate(robot,
                                       np_.asarray(structurematrix),
                                       np_.asarray(wrench),
                                       **kwargs)

    def __call__(self,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        return self.evaluate(robot, structurematrix, wrench, **kwargs)
