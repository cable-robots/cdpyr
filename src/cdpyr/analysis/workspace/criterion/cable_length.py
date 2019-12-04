import numpy as _np

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CableLength(_criterion.Criterion):
    kinematics: '_kinematics.Algorithm'
    _limits: Vector

    def __init__(self,
                 kinematics: '_kinematics.Algorithm',
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
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs):
        try:
            kinematics = self.kinematics.backward(robot, pose)
        except BaseException:
            return False
        else:
            return (_np.logical_and(self._limits[0, :] <= kinematics.lengths,
                                    kinematics.lengths <= self._limits[1,
                                                          :])).all()


__all__ = [
        'CableLength',
]
