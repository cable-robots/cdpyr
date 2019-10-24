from typing import Dict

from enum import Enum

from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import (
    cable_length,
    collision,
    interference,
    singularities,
    wrench_closure,
    wrench_feasible,
)
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as   _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Criterion(Enum):
    CABLE_LENGTH = [cable_length]
    COLLISION = [collision]
    INTERFERENCE = [interference]
    SINGULARITIES = [singularities]
    WRENCH_CLOSURE = [wrench_closure]
    WRENCH_FEASIBLE = [wrench_feasible]

    _parameters: Dict

    def __init__(self, *args):
        try:
            for name, value in args[0][0].__vars__:
                setattr(self, name, value() if callable(value) else value)
        except AttributeError as AttributeException:
            pass

    @property
    def implementation(self):
        return self._value_[0]

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Calculator'):
        self._kinematics = kinematics

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

    def setup(self, robot):
        self.implementation.setup(self, robot)

    def teardown(self, robot):
        self.implementation.teardown(self, robot)

    def evaluate(self,
                 robot: '_robot.Robot',
                 calculator: '_calculator.Calculator',
                 pose: '_pose.Pose'):
        """
        Evaluate validity of the current pose for the criterion it represents.

        Parameters
        ----------
        robot : Robot
            Robot document, available in case parameters or values need to be
            retrieved from it.
        pose : Pose
            Current pose to check.
        kwargs : dict
            Additional parameters that give the criterion more meaning.
        """

        return self.implementation.evaluate(self, robot, calculator, pose)

    def __dir__(self):
        """
        We extend the list of properties of this object by the content of
        list `__vars__` of the underlying algorithm. Unfortunately, this only
        works when in the console and not in an IDE like PyCharm.

        Returns
        -------
        dir : list
        """
        keys = super(Enum, self).__dir__()
        try:
            keys = keys + self.implementation.__vars__
        except AttributeError as AttributeException:
            pass

        return keys
