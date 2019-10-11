from typing import Sequence, Union

from cdpyr.analysis.structurematrix.algorithm.algorithm import Algorithm
from cdpyr.motion import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


class MotionPattern_3T(Algorithm):

    @classmethod
    def calculate(cls,
                  platform: '_platform.Platform',
                  uis: Matrix,
                  pose: '_pose.Pose' = None):
        return uis[0:3, :]
