from typing import Sequence, Union

import numpy as np_

from cdpyr.analysis.structurematrix.algorithm.algorithm import Algorithm
from cdpyr.motion import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


class StructureMatrix2R3T(Algorithm):

    @classmethod
    def calculate(cls,
                  platform: '_platform.Platform',
                  uis: Matrix,
                  pose: '_pose.Pose' = None):
        return np_.vstack((
            uis,
            np_.cross(
                pose.angular.dcm.dot(
                    platform.bi
                ),
                uis,
                axis=0
            )[0:platform.motionpattern.dof_rotation, :]
        ))
