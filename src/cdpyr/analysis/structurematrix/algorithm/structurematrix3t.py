from typing import Sequence, Union

from cdpyr.analysis.structurematrix.algorithm.algorithminterface import AlgorithmInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


class StructureMatrix3T(AlgorithmInterface):

    @classmethod
    def evaluate(cls,
                 platform: '_platform.Platform',
                 uis: Matrix,
                 pose: '_pose.Pose' = None):
        return uis[0:3, :]
