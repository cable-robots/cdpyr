from typing import List, Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm.algorithm import Algorithm as \
    KinematicsInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import kinematicchain as _kinematicchain, robot as _robot
from cdpyr.typing import Matrix, Num


class Standard(KinematicsInterface):

    def forward(self,
                robot: '_robot.Robot',
                pose: Union[Sequence['_pose.Pose'], '_pose.Pose']
                ):
        raise NotImplementedError()

    def backward(self,
                 robot: '_robot.Robot',
                 pose: Union[Sequence['_pose.Pose'], '_pose.Pose']
                 ) -> Tuple[np_.ndarray, np_.ndarray, np_.ndarray]:

        # validate all inputs
        self._validate_inputs_backward(robot=robot, pose=pose)

        # turn single entry pose into something iterable
        poses = pose if isinstance(pose, Sequence) else [pose]

        # init return values
        cable_lengths: List[Num] = []
        cable_vectors: List[Vector] = []
        unit_vectors: List[Vector] = []

        # loop over each kinematic chain
        for idx, kc in enumerate(robot.kinematic_chains):
            kc: '_kinematicchain.KinematicChain'
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

        return cable_lengths, unit_vectors, cable_vectors


Standard.__repr__ = make_repr()

__all__ = [
    'Standard'
]
