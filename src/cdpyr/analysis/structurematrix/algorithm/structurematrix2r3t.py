import numpy as np_

from cdpyr.analysis.structurematrix.algorithm.algorithminterface import \
    AlgorithmInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


class StructureMatrix2R3T(AlgorithmInterface):

    @classmethod
    def evaluate(cls,
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
