from __future__ import annotations

from abc import abstractmethod

from cdpyr.analysis import evaluator as _evaluator
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Criterion(_evaluator.PoseEvaluator):

    def evaluate(self, robot: _robot.Robot, pose: _pose.Pose, **kwargs):
        """
        Public method to evaluate the pose criterio
        Parameters
        ----------
        robot
        pose
        kwargs

        Returns
        -------

        """
        # TODO remove this check
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Workspace criteria are currently not implemented for '
                    'robots '
                    'with more than one platform.')

        # pass down to the criterion's actual evaluation implementation
        return self._evaluate(robot, pose, **kwargs)

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def _evaluate(self, robot: _robot.Robot, pose: _pose.Pose, **kwargs):
        raise NotImplementedError()


__all__ = [
        'Criterion',
]
