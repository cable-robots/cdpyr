from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr
from scipy.linalg import null_space

from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motion_pattern as _motion_pattern
from cdpyr.robot import platform as _platform, robot as _robot
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Calculator(object):
    _MAPPING: dict

    def __init__(self):
        self._MAPPING = {
            _motion_pattern.MotionPattern.MP_1T.name:   self._mp_1t,
            _motion_pattern.MotionPattern.MP_2T.name:   self._mp_2t,
            _motion_pattern.MotionPattern.MP_3T.name:   self._mp_3t,
            _motion_pattern.MotionPattern.MP_1R2T.name: self._mp_1r2t,
            _motion_pattern.MotionPattern.MP_2R3T.name: self._mp_2r3t,
            _motion_pattern.MotionPattern.MP_3R3T.name: self._mp_3r3t,
        }

    def evaluate(self,
                 robot: '_robot.Robot',
                 uis: Union[Matrix, Sequence[Matrix]],
                 pose: Optional[
                     Union['_pose.Pose', Sequence['_pose.Pose']]] = None,
                 ) -> 'Result':
        if robot.num_platforms > 1:
            raise NotImplementedError(
                'Currently, the structure matrix can only be computed for '
                'single-platform cable robots'
            )

        # get pose of only the first platform
        pose = pose[0] if isinstance(pose, Sequence) else pose

        # get uis of only the first platform
        uis = uis[0] if isinstance(uis, Sequence) else uis

        # TODO implement here the logic to return the extended structure
        #  matrix for multi-platform CDPRs

        # calculate the platforms structure matrix
        return Result(pose, self._MAPPING[
            robot.platforms[0].motionpattern.name](pose,
                                                   robot.platforms[0],
                                                   uis)
                      )

    def _mp_1t(self,
               pose: '_pose.Pose',
               platform: '_platform.Platform',
               uis: Matrix):
        return uis[0:1, :]

    def _mp_2t(self,
               pose: '_pose.Pose',
               platform: '_platform.Platform',
               uis: Matrix):
        return uis[0:2, :]

    def _mp_3t(self,
               pose: '_pose.Pose',
               platform: '_platform.Platform',
               uis: Matrix):
        return uis[0:3, :]

    def _mp_1r2t(self,
                 pose: '_pose.Pose',
                 platform: '_platform.Platform',
                 uis: Matrix):
        return np_.vstack(
            (
                uis,
                np_.cross(
                    pose.angular.dcm.dot(
                        platform.bi
                    )[0:platform.motionpattern.dof_translation, :],
                    uis,
                    axis=0
                )
            )
        )

    def _mp_2r3t(self,
                 pose: '_pose.Pose',
                 platform: '_platform.Platform',
                 uis: Matrix):
        return np_.vstack(
            (
                uis,
                np_.cross(
                    pose.angular.dcm.dot(
                        platform.bi
                    ),
                    uis,
                    axis=0
                )[0:platform.motionpattern.dof_rotation, :]
            )
        )

    def _mp_3r3t(self,
                 pose: '_pose.Pose',
                 platform: '_platform.Platform',
                 uis: Matrix):
        return np_.vstack(
            (
                uis,
                np_.cross(
                    pose.angular.dcm.dot(
                        platform.bi
                    ),
                    uis,
                    axis=0
                )
            )
        )


Calculator.__repr__ = make_repr()


class Result(object):
    _matrix: np_.ndarray
    _nullspace: np_.ndarray
    _pose: '_pose.Pose'

    def __init__(self, pose: '_pose.Pose', matrix: Matrix):
        self.pose = pose
        self._matrix = matrix
        self._nullspace = None

    @property
    def matrix(self):
        return self._matrix

    @property
    def nullspace(self):
        if self._nullspace is None:
            self._nullspace = null_space(self.matrix)

        return self._nullspace

    @property
    def is_singular(self):
        return np_.linalg.matrix_rank(self.matrix) >= self.matrix.shape[0]


Result.__repr__ = make_repr(
    'matrix',
    'nullspace',
    'pose',
)

__all__ = [
    'Calculator',
    'Result',
]
