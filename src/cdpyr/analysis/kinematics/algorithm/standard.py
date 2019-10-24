from typing import Sequence

import numpy as np_

from cdpyr.analysis.kinematics import kinematics as _calculator
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import (
    kinematicchain as _kinematicchain,
    platform as _platform,
    robot as _robot,
)
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def forward(calculator: '_calculator.Calculator',
            robot: '_robot.Robot',
            joints: Sequence[Vector]):
    pass


def backward(calculator: '_calculator.Calculator',
             robot: '_robot.Robot',
             pose: Sequence['_pose.Pose']):
    # init return values
    cable_lengths = []
    unit_vectors = []

    # some type hinting
    kcs: _kinematicchain.KinematicChainList = robot.kinematic_chains
    kc: _kinematicchain.KinematicChain
    platform: _platform.Platform

    # loop over each platform and solve its inverse kinematics
    for idx, platform in enumerate(robot.platforms):
        # find the platform's kinematic chains
        kc = kcs.with_platform(platform)

        # get the platform position and rotation
        pos, rot = pose[idx].position

        # solve the vector loop for the given platform
        cable_vectors = _vector_loop(
            pos,
            rot,
            np_.vstack([ai.position for ai in kc.frame_anchor]).T,
            np_.vstack([bi.position for bi in platform.anchors]).T,
        )
        # strip additional spatial dimensions
        cable_vectors = cable_vectors[
                        0:platform.motionpattern.dof_translation, :]

        # calculate norm of columns i.e., cable lengths
        cable_length = np_.linalg.norm(cable_vectors, axis=0)
        cable_lengths.append(cable_length)

        # and calculate the normalized direction vectors
        unit_vector = cable_vectors / cable_length
        # to avoid a division by zero yielding `NaN`, we will set all unit
        # vectors to zero where the cable length is zero. technically,
        # this case is not well-defined, however, from the standard
        # kinematics algorithm there is no force transmitted, so ui == 0 in
        # this case
        unit_vector[:, cable_length == 0] = 0
        unit_vectors.append(unit_vector)

    if robot.num_platforms == 1:
        return cable_lengths[0], unit_vectors[0]

    return cable_lengths, unit_vectors


def _vector_loop(pos, rot, ai, bi):
    return ai - (pos[:, np_.newaxis] + rot.dot(bi))
