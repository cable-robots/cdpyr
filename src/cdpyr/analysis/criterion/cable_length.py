from __future__ import annotations

import numpy as _np

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Vector
from cdpyr.exceptions import InvalidPoseException

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CableLength(_criterion.Criterion):
    kinematics: _kinematics.Algorithm
    _limits: Vector

    def __init__(self,
                 kinematics: _kinematics.Algorithm,
                 limits: Vector = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.kinematics = kinematics
        self.limits = limits if limits is not None else [0, _np.inf]

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits: Vector):
        limits = _np.asarray(limits)

        # ensure `limits` is a 2xK matrix
        if limits.ndim == 1:
            limits = limits[:, _np.newaxis]

        # sort `limits` such that the first row is minimum and second row is
        # maximum
        self._limits = _np.sort(limits, axis=0)

    @limits.deleter
    def limits(self):
        del self._limits

    def _evaluate(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs):
        try:
            kinematics = self.kinematics.backward(robot, pose)
        except Exception:
            raise InvalidPoseException(f'Error solving the inverse kinematics at pose {pose}')

        lengths = kinematics.lengths
        limits = self._limits

        if any(_np.logical_or(lengths < limits[0,:], limits[1,:] < lengths)):
            idx_violated = _np.unique(_np.hstack(
                    (_np.where(lengths < limits[0,:])[0],
                     _np.where(limits[1,:] < lengths)[0])))

            raise InvalidPoseException(f'cable lengths violated for cables {idx_violated}')


__all__ = [
        'CableLength',
]
