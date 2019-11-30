from abc import abstractmethod

from cdpyr.analysis import evaluator as _evaluator
from cdpyr.analysis.structure_matrix import structure_matrix_result as _result
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(_evaluator.Evaluator):

    def evaluate(self,
                 platform: '_platform.Platform',
                 pose: '_pose.Pose',
                 directions: Matrix) -> '_result.StructureMatrixResult':
        return _result.StructureMatrixResult(pose,
                                             **self._evaluate(platform, pose,
                                                              directions))

    @abstractmethod
    def _evaluate(self,
                  platform: '_platform.Platform',
                  pose: '_pose.Pose',
                  directions: Matrix) -> dict:
        raise NotImplementedError()


__all__ = [
    'Algorithm',
]
