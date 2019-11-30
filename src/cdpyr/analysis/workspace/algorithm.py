from abc import ABC, abstractmethod

from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace import workspace_result as _result
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(ABC):
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self._archetype = archetype
        self._criterion = criterion

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion

    def evaluate(self, robot: '_robot.Robot') -> '_result.WorkspaceResult':
        try:
            if not isinstance(self._archetype, _archetype.Archetype):
                raise AttributeError(
                    f'Failed starting calculation of the workspace. Missing '
                    f'or invalid value for attribute `archetype`. Please set '
                    f'a valid archetype object, then re-run evaluation of the '
                    f'workspace.')

            if not isinstance(self._criterion, _criterion.Criterion):
                raise AttributeError(
                    f'Failed starting calculation of the workspace. Missing '
                    f'or invalid value for attribute `criterion`. Please set '
                    f'a valid criterion object, then re-run evaluation of the '
                    f'workspace.')
        except (AttributeError, ValueError) as EvaluationE:
            raise RuntimeError(
                'Could not determine workspace due to assertion failed in '
                'setting up the workspace calculator. Please review your '
                'code.') from EvaluationE

        try:
            # now finally, evaluate the workspace
            return self._evaluate(robot)
        except BaseException as BaseE:
            raise RuntimeError('Could not determine workspace.') from BaseE

    @abstractmethod
    def _evaluate(self, robot: '_robot.Robot') -> '_result.WorkspaceResult':
        raise NotImplementedError()


__all__ = [
    'Algorithm',
]
