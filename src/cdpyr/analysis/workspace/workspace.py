from typing import Any, AnyStr, Dict

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Workspace(object):
    _archetype: '_archetype.Archetype'
    _method: '_method.Method'
    _criterion: '_criterion.Criterion'
    _parameters: Dict[AnyStr, Any]
    __kinematics: '_kinematics.Calculator'

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 method: '_method.Method',
                 criterion: '_criterion.Criterion',
                 *args,
                 kinematics: '_kinematics.Calculator' = None,
                 **kwargs):
        self.archetype = archetype
        self.method = method
        self.criterion = criterion
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
    def criterion(self):
        return self._criterion

    @criterion.setter
    def criterion(self, criterion: '_criterion.Criterion'):
        self._criterion = criterion

    @criterion.deleter
    def criterion(self):
        del self._criterion

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
        # setup the criterion
        self.criterion.setup(robot)

        # then, dispatch to the workspace method algorithm to calculate the
        # workspace
        workspace = self.method.evaluate(robot,
                                         self,
                                         self.archetype,
                                         self.criterion)

        # after the workspace is calculated, we will tear down the criterion
        self.criterion.teardown(robot)

        # and return the result
        return workspace
