from enum import Enum
from typing import Sequence

from magic_repr import make_repr

from cdpyr.algorithms.structurematrix.algorithm import StructureMatrixAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class Solver(object):

    def _call__(self,
                robot: Robot,
                pose: Pose
                ):
        # make sure we are dealing with a sequence of poses
        poses = pose if isinstance(pose, Sequence) else [pose]

        # ensure we have just as many poses as platforms
        if len(robot.platforms) != len(poses):
            raise ValueError('number of poses must match number of robot platforms.')

        # init return value
        structurematrices = []

        # loop over each platform and calculate its structure matrix
        for idx, platform in enumerate(robot.platforms):
            # get platform's pose
            pose = poses[idx]
            # calculate the platforms structure matrix
            structurematrices.append(platform.motionpattern.structure_matrix(pose))



Solver.__repr__ = make_repr()

__all__ = [
    'Solver'
]
