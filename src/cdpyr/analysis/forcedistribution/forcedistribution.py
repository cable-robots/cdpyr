# from typing import Sequence, Tuple, Union

import numpy as np_
from enum import Enum

from cdpyr.analysis.forcedistribution.algorithm import (
    AlgorithmInterface as ForceDistributionAlgorithm,
    ClosedForm,
    ClosedFormImproved,
    Dykstra,
)
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ForceDistribution(Enum):
    CLOSED_FORM = (ClosedForm())
    CLOSED_FORM_IMPROVED = (ClosedFormImproved())
    DYKSTRA = (Dykstra())

    @property
    def algorithm(self) -> ForceDistributionAlgorithm:
        return self._value_

    def calculate(self,
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

        return self.algorithm.calculate(robot,
                                        np_.asarray(structurematrix),
                                        np_.asarray(wrench),
                                        **kwargs)

    def __call__(self,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        return self.calculate(robot, structurematrix, wrench, **kwargs)
