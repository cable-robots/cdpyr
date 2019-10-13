from abc import ABC, abstractmethod

from cdpyr.motion import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


class AlgorithmInterface(ABC):

    @classmethod
    @abstractmethod
    def evaluate(cls,
                 platform: '_platform.Platform',
                 uis: Matrix,
                 pose: '_pose.Pose' = None):
        raise NotImplementedError()
