from typing import Union

import numpy as _np

from cdpyr.analysis.force_distribution import algorithm as \
    _force_distribution
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class WrenchFeasible(_criterion.Criterion):
    _wrench: Vector
    _force_distribution: '_force_distribution.Algorithm'

    def __init__(self,
                 force_distribution: '_force_distribution.Algorithm',
                 wrench: Union[Num, Vector]):
        self.wrench = wrench
        self.force_distribution = force_distribution

    @property
    def force_distribution(self):
        return self._force_distribution

    @force_distribution.setter
    def force_distribution(self,
                           force_distribution: '_force_distribution.Algorithm'):
        self._force_distribution = force_distribution

    @force_distribution.deleter
    def force_distribution(self):
        del self._force_distribution

    @property
    def wrench(self):
        return self._wrench

    @wrench.setter
    def wrench(self, wrench: Vector):
        # anything to a numpy array
        wrench = _np.asarray(wrench)
        # scalar to vector
        if wrench.ndim == 0:
            wrench = _np.asarray([wrench])
        # vector to matrix
        if wrench.ndim == 1:
            wrench = wrench[:, _np.newaxis]

        self._wrench = wrench

    @wrench.deleter
    def wrench(self):
        del self._wrench

    def _evaluate(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs):
        try:
            [self.force_distribution.evaluate(robot, pose, wrench)
             for wrench in self.wrench.T]
        except (ArithmeticError, ValueError):
            flag = False
        else:
            flag = True
        finally:
            return flag

    def _validate(self, robot: '_robot.Robot'):
        if not isinstance(self.force_distribution,
                          _force_distribution.Algorithm):
            raise AttributeError(
                f'Missing value for `force_distribution` property. Please set '
                f'a force distribution algorithm on the `WrenchFeasible` '
                f'object, then calculate the workspace again')

        if not isinstance(self.wrench, _np.ndarray):
            raise AttributeError(
                f'Missing value for attribute `wrench`. Please set a wrench '
                f'on the `WrenchFeasible` object, then calculate the '
                f'workspace again')

        if self.wrench.shape[0] != robot.num_dof:
            raise AttributeError(
                f'Invalid size of wrench. Should be a `({robot.num_dof},'
                f'K), but received `{self.wrench.shape}`.')


__all__ = [
    'WrenchFeasible',
]
