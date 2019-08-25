from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.motion.pose import Pose
from cdpyr.robot.kinematicchain import KinematicChain
from cdpyr.robot.robot import Robot


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
        cable_vectors = []
        cable_lengths = []
        unit_vectors = []

        # loop over each kinematic chain
        for idx, kc in enumerate(robot.kinematic_chains):
            kc: KinematicChain
            # find the platforms index
            idx_platform = robot.platforms.index(kc.platform)
            # get all information for the kinematic chain
            pose = poses[idx_platform]
            r, R = pose.position
            # cable direction vector
            cable_vectors.append(
                kc.frame_anchor.position
                -
                (
                    r
                    +
                    R.dot(
                        kc.platform_anchor.position
                    )
                )
            )
            # append cable length
            cable_lengths.append(np_.linalg.norm(cable_vectors[-1]))
            # unitary cable direction vector
            unit_vectors.append(cable_vectors[-1] / cable_lengths[-1])

        # here we are sorting the cable lengths back into the form that they
        # are given per platform and then per cable

        return cable_lengths, cable_vectors, unit_vectors


StandardKinematics.__repr__ = make_repr()

__all__ = [
    'StandardKinematics'
]
