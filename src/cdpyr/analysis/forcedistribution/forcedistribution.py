# from typing import Sequence, Tuple, Union

import numpy as np_
from enum import Enum

from cdpyr.analysis.forcedistribution.algorithm.algorithminterface import \
    AlgorithmInterface as ForceDistributionAlgorithm
from cdpyr.analysis.forcedistribution.algorithm.closedform import ClosedForm
from cdpyr.analysis.forcedistribution.algorithm.closedformimproved import \
    ClosedFormImproved
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class ForceDistribution(Enum):
    CLOSED_FORM = (ClosedForm())
    CLOSED_FORM_IMPROVED = (ClosedFormImproved())

    @property
    def algorithm(self) -> ForceDistributionAlgorithm:
        return self._value_

    def calculate(self,
                  robot: '_robot.Robot',
                  structurematrix: Matrix,
                  wrench: Vector,
                  **kwargs):
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
