from typing import Mapping

import numpy as _np

from cdpyr.analysis.kinematics import kinematics as _algorithm
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import (
    cable as _cable,
    kinematicchain as _kinematicchain,
    pulley as _pulley,
    robot as _robot
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor
)
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pulley(_algorithm.Algorithm):

    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Vector,
                 **kwargs) -> Mapping:
        raise NotImplementedError()

    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> Mapping:
        # init results
        swivel = []
        wrap = []
        lengths = []
        directions = []

        # extract platform position and orientation
        platform_position, platform_dcm = pose.position

        # type hinting
        frame_anchor: _frame_anchor.FrameAnchor
        platform_anchor: _platform_anchor.PlatformAnchor
        pulley: _pulley.Pulley
        cable: _cable.Cable
        chain: _kinematicchain.KinematicChain

        # loop over each kinematic chain
        for chain_index, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]
            # cable = robot.cables[chain.cable]
            pulley = frame_anchor.pulley
            frame_dcm = frame_anchor.angular.dcm
            pulley_dcm = pulley.dcm

            # frame anchor to platform (negative of conventional vector loop)
            frame_to_platform = platform_position + platform_dcm.dot(
                    platform_anchor.linear.position) - \
                                frame_anchor.linear.position

            # pulley to platform
            pulley_to_platform = pulley_dcm.T.dot(
                    frame_dcm.T.dot(frame_to_platform))

            # calculate angle of swivel
            swivel_ = _np.arctan2(pulley_to_platform[1], pulley_to_platform[0])
            swivel.append(swivel_)

            # rotation matrix from pulley to cable coordinate system
            cable_dcm = _angular.Angular.rotation_z(swivel_).dcm

            # position of the platform with respect to the roller center
            roller_center_to_platform = cable_dcm.T.dot(
                    pulley_to_platform) - _np.asarray([pulley.radius, 0, 0])

            # calculate length of cable in workspace
            length_workspace = _np.abs(_np.sqrt(_np.linalg.norm(
                    roller_center_to_platform) ** 2 - pulley.radius ** 2))

            # build matrix of cable workspace length and pulley radius
            leave_dcm = _np.asarray((
                    (pulley.radius, length_workspace),
                    (-length_workspace, pulley.radius),
            ))
            # position of the cable leave point in coordinates of the roller
            # center
            cable_leave_point = _np.linalg.solve(leave_dcm,
                                                 roller_center_to_platform[
                                                     [0, 2]])

            # "unwrapped angle"
            unwrapped = _np.arctan2(cable_leave_point[1], cable_leave_point[0])

            # append the angle of wrap
            wrap_ = _np.pi - unwrapped
            wrap.append(wrap_)

            # length of cable on the roller
            length_roller = pulley.radius * wrap_
            # store length as result
            lengths.append([length_workspace, length_roller])

            # calculate vector of cable leave point relative to the cable
            # coordinate system
            direction = (frame_dcm.dot(pulley_dcm.dot(cable_dcm.dot(
                    [pulley.radius, 0, 0] + _angular.Angular().rotation_y(
                            wrap_).dcm.dot([-pulley.radius, 0, 0])))) + (
                                 frame_anchor.linear.position - (
                                 platform_position + platform_dcm.dot(
                                 platform_anchor.linear.position))))
            directions.append(direction[
                              0:platform.motion_pattern.dof_translation] /
                              length_workspace)

        return {
                'pose':       pose,
                'lengths':    _np.asarray(lengths).T,
                'directions': _np.asarray(directions).T,
                'swivel':     _np.asarray(swivel),
                'wrap':       _np.asarray(wrap),
        }


__all__ = [
        'Pulley',
]
