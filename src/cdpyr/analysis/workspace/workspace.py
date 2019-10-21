from typing import Any, AnyStr, Dict, Sequence, Tuple

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot


class Workspace(object):
    _archetype: '_archetype.Archetype'
    _method: '_method.Method'
    _criteria: Sequence[Tuple['_criterion.Criterion', Dict[AnyStr, Any]]]
    _parameters: Dict[AnyStr, Any]
    __kinematics: '_kinematics.Calculator'

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 method: '_method.Method',
                 criteria: Sequence[
                     Tuple['_criterion.Criterion', Dict[AnyStr, Any]]],
                 *args,
                 kinematics: '_kinematics.Calculator' = None,
                 **kwargs):
        self.archetype = archetype
        self.method = method
        self.criteria = criteria
        self.parameters = kwargs
        self.kinematics = kinematics or _kinematics.Kinematics.STANDARD

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
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, criteria: Sequence[
        Tuple['_criterion.Criterion', Dict[AnyStr, Any]]]):
        # make sure every criterion is stored as tuple (Criterion, OptionsDict)
        for idx, criterion in enumerate(criteria):
            criteria[idx] = criterion if isinstance(criterion, Tuple) else (criterion, {})
            if len(criteria[idx][1]):
                for key, value in criteria[idx][1].items():
                    setattr(criteria[idx][0], key, value)

        self._criteria = criteria

    @criteria.deleter
    def criteria(self):
        del self._criteria

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Calculator'):
        self._kinematics = kinematics

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method: '_method.Method'):
        self._method = method

    @method.deleter
    def method(self):
        del self._method

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Dict[AnyStr, Any]):
        self._parameters = parameters

    @parameters.deleter
    def parameters(self):
        del self._parameters

    def evaluate(self, robot: '_robot.Robot'):
        criterion: '_criterion.Criterion'
        options: Dict[AnyStr, Any]

        # first, we will parametrize every criterion with the parameters
        # given. This will make all later evaluations quicker
        for criterion, options in self.criteria:
            criterion.setup(robot)

        # then, dispatch to the workspace method algorithm to calculate the
        # workspace
        workspace = self.method.evaluate(robot, self, self.archetype, self.criteria)

        # after the workspace is calculated, we will tear down every criterion
        for criterion, _ in self.criteria:
            criterion.teardown(robot)

        # and return the result
        return workspace
