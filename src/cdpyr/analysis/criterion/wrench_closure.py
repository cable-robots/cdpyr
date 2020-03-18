from __future__ import annotations

from typing import Optional, Union

import numpy as _np

from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.analysis.force_distribution import force_distribution as \
    _force_distribution
from cdpyr.exceptions import InvalidPoseException
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class WrenchClosure(_criterion.Criterion):
    _wrench: Vector
    _force_distribution: _force_distribution.Algorithm

    def __init__(self,
                 force_distribution: _force_distribution.Algorithm,
                 wrench: Optional[Union[Num, Vector]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        # update the force limits to be in the expected range of the wrench
        # closure algorithm
        force_distribution.force_minimum = [0]
        force_distribution.force_maximum = [_np.inf]
        self.force_distribution = force_distribution
        self.wrench = wrench

    @property
    def wrench(self):
        return self._wrench

    @wrench.setter
    def wrench(self, wrench: Vector):
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
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs):
        try:
            # determine the gravitational wrench
            wrenches = robot.gravitational_wrench(pose)[:, _np.newaxis]

            # if other wrenches are given, we will add them to the
            # gravitational wrench
            if self._wrench is not None:
                wrenches = _np.hstack((wrenches, wrenches + self._wrench)).T

            [self.force_distribution.evaluate(robot, pose, wrench)
             for wrench in wrenches.T]
        except Exception as e:
            raise InvalidPoseException(
                'pose cannot provide wrench closure.') from e


__all__ = [
        'WrenchClosure',
]
