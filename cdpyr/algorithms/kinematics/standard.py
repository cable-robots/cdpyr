from typing import List, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.kinematicchain import KinematicChain
from cdpyr.robot.robot import Robot
from cdpyr.typedefs import Num, Vector


class StandardKinematics(KinematicAlgorithm):

    def forward(self,
                robot: Robot,
                pose: Union[Sequence[Pose], Pose]
                ):
        raise NotImplementedError()

    def backward(self,
                 robot: Robot,
                 pose: Union[Sequence[Pose], Pose]
                 ):
        """
        If the robot contains multiple platforms, then the number of poses
        must be equal to the number of platforms

        :param robot:
        :param pose:
        :return:
        """

        # validate all inputs
        self._validate_inputs_backward(robot=robot, pose=pose)

        # turn single entry poses into something iterable
        poses = pose if isinstance(pose, Sequence) else [pose]

        # init return values
        cable_lengths: List[Num] = []
        cable_vectors: List[Vector] = []
        unit_vectors: List[Vector] = []

        # loop over each kinematic chain
        for idx, kc in enumerate(robot.kinematic_chains):
            kc: KinematicChain
            # find the platforms index
            idx_platform = robot.platforms.index(kc.platform)
            # get all information for the kinematic chain
            pose = poses[idx_platform]
            r, R = pose.position
            # cable direction vector
            cable_vector = kc.frame_anchor.position - (
                r
                +
                R.dot(kc.platform_anchor.position)
            )
            # append to list
            cable_vectors.append(cable_vector)
            # append cable length
            cable_length = np_.linalg.norm(cable_vector)
            cable_lengths.append(cable_length)
            # unitary cable direction vector
            unit_vectors.append(cable_vector / cable_length)

        # here we are sorting the cable lengths back into the form that they
        # are given per platform and then per cable

        return cable_lengths, cable_vectors, unit_vectors


StandardKinematics.__repr__ = make_repr()

__all__ = [
    'StandardKinematics'
]
