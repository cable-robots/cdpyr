import numpy as np_

from cdpyr.analysis.structurematrix import structurematrix as _structurematrix
from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__vars__ = [
]


def setup(criterion: '_criterion.Criterion',
          robot: '_robot.Robot'):
    criterion.structurematrix = _structurematrix.StructureMatrix()


def teardown(criterion: '_criterion.Criterion',
             robot: '_robot.Robot'):
    pass


def evaluate(criterion: '_criterion.Criterion',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             pose: '_pose.Pose'):
    # evaluate inverse kinematics at the current pose
    _, uis = calculator.kinematics.backward(robot, pose)

    # get the structure matrix
    structmat: np_.ndarray = criterion.structurematrix.evaluate(robot, uis,
                                                                pose)

    # according to Pott.2018, a pose is singular if the structure matrix's
    # rank is smaller than the number of degrees of freedom i.e., the structure
    # matrix's number of rows
    return np_.linalg.matrix_rank(structmat) >= structmat.shape[0]
    # get the structure matrix
    structmat: np_.ndarray = criterion.structurematrix.evaluate(robot, uis,
                                                                pose)

    # according to Pott.2018, a pose is singular if the structure matrix's
    # rank is smaller than the number of degrees of freedom i.e., the structure
    # matrix's number of rows
    return np_.linalg.matrix_rank(structmat) >= structmat.shape[0]
