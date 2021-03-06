from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Calculator',
]

from typing import AnyStr, Dict

import numpy as _np

from cdpyr.analysis import evaluator as _evaluator
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.structure_matrix import (
    motion_pattern_1r2t as _structure_matrix_1r2t,
    motion_pattern_1t as _structure_matrix_1t,
    motion_pattern_2r3t as _structure_matrix_2r3t,
    motion_pattern_2t as _structure_matrix_2t,
    motion_pattern_3r3t as _structure_matrix_3r3t,
    motion_pattern_3t as _structure_matrix_3t,
    structure_matrix as _structure_matrix,
)
from cdpyr.motion import pattern as _pattern, pose as _pose
from cdpyr.robot import robot as _robot


class Calculator(_evaluator.PoseEvaluator):
    kinematics: _kinematics.Algorithm
    resolver: Dict[AnyStr, _structure_matrix.Algorithm]

    def __init__(self,
                 kinematics: _kinematics.Algorithm,
                 resolver: Dict[AnyStr, _structure_matrix.Algorithm] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.kinematics = kinematics
        if resolver is None:
            resolver = {
                    _pattern.MP_1T:
                        _structure_matrix_1t.MotionPattern1T(),
                    _pattern.MP_2T:
                        _structure_matrix_2t.MotionPattern2T(),
                    _pattern.MP_3T:
                        _structure_matrix_3t.MotionPattern3T(),
                    _pattern.MP_1R2T:
                        _structure_matrix_1r2t.MotionPattern1R2T(),
                    _pattern.MP_2R3T:
                        _structure_matrix_2r3t.MotionPattern2R3T(),
                    _pattern.MP_3R3T:
                        _structure_matrix_3r3t.MotionPattern3R3T(),
            }
        self.resolver = resolver

    def evaluate(self,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 *args,
                 **kwargs) -> _structure_matrix.Result:
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Structure matrices are currently not implemented for '
                    'robots with more than one platform.'
            )

        # solve inverse kinematics
        kinematics = self.kinematics.backward(robot, pose)

        # platform index (to fake the `for platform` loop)
        platform_index = 0

        # get the current  platform
        platform = robot.platforms[platform_index]

        return self.resolver[platform.motion_pattern].evaluate(
                pose,
                platform.bi[[kc.platform_anchor for kc in robot.kinematic_chains.with_platform(platform_index)], :],
                kinematics.directions)
