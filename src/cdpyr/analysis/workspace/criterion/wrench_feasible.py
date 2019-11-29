from typing import (
    Union,
    Optional
)

import numpy as _np

from cdpyr.analysis.force_distribution import algorithm as \
    _force_distribution
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.typing import (
    Num,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class WrenchFeasible(_criterion.Criterion):
    _wrench: Vector
    force_distribution: '_force_distribution.Algorithm'

    def __init__(self,
                 force_distribution: '_force_distribution.Algorithm',
                 wrench: Optional[Union[Num, Vector]] = None):
        self.force_distribution = force_distribution
        self.wrench = wrench

    @property
    def wrench(self):
        return self._wrench

    @wrench.setter
    def wrench(self, wrench: Vector):
        # TODO We should allow here for empty wrenches and if so, then take
        #  the wrench as gravity wrench from the platform/robot
        if wrench is not None:
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
             for wrench in self._wrench.T]
        except Exception:
            flag = False
        else:
            flag = True
        finally:
            return flag


__all__ = [
    'WrenchFeasible',
]
