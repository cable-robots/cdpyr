from abc import ABC, abstractmethod

from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace import result as _result
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(ABC):
    _kinematics: '_kinematics.Algorithm'
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'

    def __init__(self,
                 kinematics: '_kinematics.Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self.archetype = archetype
        self.criterion = criterion
        self.kinematics = kinematics

    @property
    def archetype(self):
        return self._archetype

    @archetype.setter
    def archetype(self, archetype: '_archetype.Archetype'):
        self._archetype = archetype

    @archetype.deleter
    def archetype(self):
        del self._archetype

    @property
    def criterion(self):
        return self._criterion

    @criterion.setter
    def criterion(self, criterion: '_criterion.Criterion'):
        try:
            criterion.kinematics = self._kinematics
        except AttributeError as AttributeE:
            pass
        self._criterion = criterion

    @criterion.deleter
    def criterion(self):
        del self._criterion

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Algorithm'):
        self._kinematics = kinematics
        try:
            self.criterion.kinematics = kinematics
        except AttributeError as AttributeE:
            pass

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

    def evaluate(self, robot: '_robot.Robot') -> '_result.Result':
        try:
            if not isinstance(self.archetype, _archetype.Archetype):
                raise AttributeError(
                    f'Failed starting calculation of the workspace. Missing '
                    f'or invalid value for attribute `archetype`. Please set '
                    f'a valid archetype object, then re-run evaluation of the '
                    f'workspace.')

            if not isinstance(self.criterion, _criterion.Criterion):
                raise AttributeError(
                    f'Failed starting calculation of the workspace. Missing '
                    f'or invalid value for attribute `criterion`. Please set '
                    f'a valid criterion object, then re-run evaluation of the '
                    f'workspace.')

            # further validation as required by the concrete workspace evaluator
            self._validate(robot)
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
    def _evaluate(self, robot: '_robot.Robot') -> '_result.Result':
        raise NotImplementedError

    @abstractmethod
    def _validate(self, robot):
        # for now, I do not know how to handle cases where the robot has less
        # than 3 DOF i.e., where the hull cannot be applied to 3 coordinates
        if robot.num_dof < 3:
            raise ValueError(
                f'Expected robot to have at least 3 degrees of freedom but '
                f'was given a robot with `{robot.num_dof}` degrees of freedom.')


__all__ = [
    'Algorithm',
]
