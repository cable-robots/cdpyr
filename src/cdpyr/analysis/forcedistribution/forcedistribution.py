from typing import Callable

import numpy as np_
from enum import Enum

from cdpyr import validator as _validator
from cdpyr.analysis.forcedistribution import algorithm
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num, Vector


class ForceDistribution(Enum):
    CLOSED_FORM = [algorithm.closed_form]
    CLOSED_FORM_IMPROVED = [algorithm.closed_form_improved]
    DYKSTRA = [algorithm.dykstra]

    @property
    def implementation(self) -> Callable:
        return self._value_[0]

    def evaluate(self,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        # ensure structure matrix is landscape rectangular
        _validator.linalg.landspace(structurematrix, 'structurematrix')

        # get force limits from the passed arguments
        force_min, force_max = self._parse_force_limits(
            structurematrix.shape[1], **kwargs)
        kwargs.update(force_min=force_min, force_max=force_max)

        return self.implementation.evaluate(self,
                                            np_.asarray(structurematrix),
                                            np_.asarray(wrench),
                                            **kwargs)

    @classmethod
    def _parse_force_limits(cls,
                            num_cable: Num,
                            **kwargs):
        # get parameters passed by the user
        force_min: Vector = np_.asarray(kwargs.pop('force_min', 0))
        force_max: Vector = np_.asarray(kwargs.pop('force_max', np_.inf))

        # turn scalar force limits into (1,) arrays
        if force_min.ndim == 0:
            force_min = np_.asarray([force_min])
        if force_max.ndim == 0:
            force_max = np_.asarray([force_max])

        # pad force limits up to the number of cables
        force_min = np_.pad(force_min,
                            (0, num_cable - force_min.size),
                            constant_values=(0, force_min[0])
                            )
        force_max = np_.pad(force_max,
                            (0, num_cable - force_max.size),
                            constant_values=(0, force_max[0])
                            )

        # finally validate these values
        _validator.numeric.greater_than_or_equal_to(force_min, 0, 'force_min')
        _validator.numeric.less_than_or_equal_to(force_max, np_.inf,
                                                 'force_max')

        return force_min, force_max
