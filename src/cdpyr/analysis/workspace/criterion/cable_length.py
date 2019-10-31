import numpy as _np

from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CableLength(_criterion.Criterion):
    _kinematics: '_kinematics.Algorithm'
    _limits: Vector

    def __init__(self,
                 kinematics: '_kinematics.Algorithm',
                 limits: Vector = None):
        self.kinematics = kinematics
        self.limits = limits if limits is not None else [0, _np.inf]

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Algorithm'):
        self._kinematics = kinematics

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

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

    def _validate(self, robot: '_robot.Robot'):
        if not isinstance(self.kinematics, _kinematics.Algorithm):
            raise AttributeError(
                f'Missing value for `kinematics` property. Please set a '
                f'kinematics algorithm in the `CableLength` object, '
                f'then calculate the workspace again')


__all__ = [
    'CableLength',
]
