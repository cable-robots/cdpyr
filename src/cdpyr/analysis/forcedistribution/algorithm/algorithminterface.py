from typing import Union

import numpy as np_
from abc import ABC, abstractmethod

from cdpyr import validator as _validator
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num, Vector


class AlgorithmInterface(ABC):

    @classmethod
    @abstractmethod
    def evaluate(cls,
                 robot: '_robot.Robot',
                 structurematrix: Matrix,
                 wrench: Vector,
                 **kwargs):
        raise NotImplementedError()

    @classmethod
    def _parse_force_limits(cls,
                            num_cable: Num,
                            force_min: Union[Num, Vector],
                            force_max: Union[Num, Vector]):
        # get parameters passed by the user
        force_min: Vector = np_.asarray(force_min)
        force_max: Vector = np_.asarray(force_max)

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
        _validator.numeric.less_than_or_equal_to(force_max, np_.inf, 'force_max')

        return force_min, force_max
