import numpy as np_

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__vars__ = [
    ('limits', np_.asarray((0, np_.inf))),
]


def setup(criterion: '_criterion.Criterion',
          robot: '_robot.Robot'):
    # adjust limits to be of the right type and shape
    limits = np_.asarray(criterion.limits)

    # get limits stacked so that the first row is minimum, and the second row
    # is maximum
    if limits.ndim == 2:
        limits = limits.T
    else:
        limits = np_.repeat(limits[:, np_.newaxis], robot.num_cables, axis=1)
    # and push back in the right shape
    criterion.limits = limits


def teardown(criterion: '_criterion.Criterion',
             robot: '_robot.Robot'):
    pass


def evaluate(criterion: '_criterion.Criterion',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             pose: '_pose.Pose'):
    # evaluate inverse kinematics at the current pose
    lengths, _ = calculator.kinematics.backward(robot, pose)

    # now it's just logical comparison of the cable lengths
    return np_.logical_and(criterion.limits[0, :] <= lengths,
                           lengths <= criterion.limits[1, :]).all()
