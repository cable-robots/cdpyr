from __future__ import annotations

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.structure_matrix import calculator as _structure_matrix
from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Singularities(_criterion.Criterion):
    _kinematics: _kinematics.Algorithm
    _structure_matrix: _structure_matrix.Calculator

    def __init__(self, kinematics: _kinematics.Algorithm, **kwargs):
        super().__init__(**kwargs)
        self._kinematics = kinematics
        self._structure_matrix = _structure_matrix.Calculator(self._kinematics)

    @property
    def kinematics(self):
        return self._kinematics

    def _evaluate(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs):
        # according to Pott.2018, a pose is singular if the structure
        # matrix's rank is smaller than the number of degrees of freedom
        # i.e., the structure matrix's number of rows
        return self._structure_matrix.evaluate(robot, pose).is_singular


__all__ = [
        'Singularities',
]
