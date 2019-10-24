from typing import Sequence

import numpy as np_

from cdpyr.analysis.forcedistribution import forcedistribution as \
    _forcedistribution
from cdpyr.analysis.structurematrix import structurematrix as _structurematrix
from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__vars__ = [
    ('wrench', np_.zeros((6,))),
    ('force_min', 1),
    ('force_max', 10),
    ('forcedistribution',
     _forcedistribution.ForceDistribution.CLOSED_FORM_IMPROVED),
]


def setup(criterion: '_criterion.Criterion',
          robot: '_robot.Robot'):
    criterion.structurematrix = _structurematrix.StructureMatrix()
    wrench = np_.asarray(criterion.wrench
                         if isinstance(criterion.wrench, Sequence)
                         else [criterion.wrench])
    if wrench.ndim == 0:
        wrench = np_.asarray([wrench])
    if wrench.ndim == 1:
        wrench = np_.vstack((wrench, wrench)).T
        # wrench = wrench[:,np_.newaxis]
    criterion.wrench = np_.asarray(wrench)


def teardown(criterion: '_criterion.Criterion',
             robot: '_robot.Robot'):
    pass


def evaluate(criterion: '_criterion.Criterion',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             pose: '_pose.Pose'):
    # evaluate inverse kinematics at the current pose
    _, uis = calculator.kinematics.backward(robot, pose)

    # get structure matrix
    structmat = criterion.structurematrix.evaluate(robot, uis, pose)

    try:
        [criterion.forcedistribution.evaluate(
            robot,
            structmat,
            wrench,
            force_min=criterion.force_min,
            force_max=criterion.force_max
        ) for wrench in criterion.wrench.T]
    except (ArithmeticError, ValueError):
        flag = False
    else:
        flag = True
    finally:
        return flag
