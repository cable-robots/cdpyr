from typing import Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm.algorithm import Algorithm as \
    KinematicsInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import (
    kinematicchain as _kinematicchain,
    platform as _platform,
    robot as _robot,
)
from cdpyr.typing import Matrix, Vector


class Standard(KinematicsInterface):

    def forward(self,
                robot: '_robot.Robot',
                lengths: Sequence[Vector]
                ) -> Union[Tuple[Vector, Matrix],
                           Tuple[Sequence[Vector], Sequence[Matrix]]]:
        raise NotImplementedError()

    def backward(self,
                 robot: '_robot.Robot',
                 pose: Sequence['_pose.Pose']
                 ) -> Union[Tuple[Vector, Matrix],
                            Tuple[Sequence[Vector], Sequence[Matrix]]]:

        # init return values
        cable_lengths = []  # np_.zeros((robot.num_kinematic_chains,))
        unit_vectors = []  # np_.zeros((3, robot.num_kinematic_chains))

        # some type hinting
        kcs: _kinematicchain.KinematicChainList = robot.kinematic_chains
        platform: _platform.Platform

        # loop over each platform and solve its inverse kinematics
        for idx, platform in enumerate(robot.platforms):
            # find the platform's kinematic chains
            kc = kcs.with_platform(platform)

            # get the platform position and rotation
            pos, rot = pose[idx].position

            # solve the vector loop for the given platform
            cable_vectors = self._vector_loop(
                pos,
                rot,
                platform.bi,
                np_.vstack(kc.frame_anchor.position).T
            )
            # calculate norm of columns i.e., cable lengths
            cable_length = np_.linalg.norm(cable_vectors, axis=0)
            cable_lengths.append(cable_length)

            # and calculate the normalized direction vectors
            unit_vectors.append(cable_vectors / cable_length)

        if robot.num_platforms == 1:
            return cable_lengths[0], unit_vectors[0]

        return cable_lengths, unit_vectors

    def _vector_loop(self, pos, rot, ai, bi):
        return ai - (pos[:, np_.newaxis] + rot.dot(bi))


Standard.__repr__ = make_repr()

__all__ = [
    'Standard'
]
