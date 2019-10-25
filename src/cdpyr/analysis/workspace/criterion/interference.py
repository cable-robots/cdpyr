from typing import  Sequence

import  itertools

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot, platform as _platform

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__vars__ = [
]


def setup(criterion: '_criterion.Criterion',
          robot: '_robot.Robot'):
    pass


def teardown(criterion: '_criterion.Criterion',
             robot: '_robot.Robot'):
    pass


def evaluate(criterion: '_criterion.Criterion',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             pose: '_pose.Pose'):
    # sequence of poses for each platform
    pose = pose if isinstance(pose, Sequence) else [pose]

    # interference of all platforms' cables with one another
    for platforms in robot.platforms.all_combinations:
        # multi-platform case where
        if len(platforms) > 1:
            pass
        # single platform case, so check only collision of its cables with each other
        else:
            pass

    # # first, solve the inverse kinematics to obtain cable directions
    # _, ui = criterion.kinematics.backward(robot, pose)
    #
    # # now, determine the start position of
    #
    # # # first, calculate tuples for each cable of (start, direction, end)
    # # for kc in robot.kinematic_chains:
    # #
    # #
    # # # # loop over all combinations of platforms
    # # platform: '_platform.Platform'
    # # for platform in robot.platforms.all_combinations:
    # #     # get platform index
    # #     idx_a =

    raise NotImplementedError
