from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Pulley',
]

import numpy as _np

from cdpyr.analysis.kinematics import kinematics as _algorithm
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion import pose as _pose
from cdpyr.robot import (
    cable as _cable,
    frame as _frame,
    kinematicchain as _kinematicchain,
    platform as _platform,
    pulley as _pulley,
    robot as _robot,
)
from cdpyr.typing import Vector


class Pulley(_algorithm.Algorithm):

    def _forward(self,
                 robot: _robot.Robot,
                 joints: Vector,
                 **kwargs) -> _algorithm.Result:
        raise NotImplementedError()

    def _backward(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs) -> _algorithm.Result:
        # type hinting
        fanchor: _frame.FrameAnchor
        panchor: _platform.PlatformAnchor
        pulley: _pulley.Pulley
        cable: _cable.Cable
        kc: _kinematicchain.KinematicChain

        # init results
        swivel = []
        wrap = []
        lengths = []
        directions = []
        cable_leave_points = []

        # number of linear dimensionality
        num_lin, _ = robot.num_dimensionality

        # loop over each kinematic chain
        for idxkc, kc in enumerate(robot.kinematic_chains):
            fanchor = robot.frame.anchors[kc.frame_anchor]
            platform = robot.platforms[kc.platform]
            panchor = platform.anchors[kc.platform_anchor]
            # cable = robot.cables[chain.cable]
            pulley = fanchor.pulley
            frame_dcm = fanchor.angular.dcm
            pulley_dcm = pulley.dcm

            # extract platform position and orientation
            ppos, prot = pose.position

            # frame anchor to platform (negative of conventional vector loop)
            frame_to_platform = ppos \
                                + prot.dot(panchor.linear.position) \
                                - fanchor.linear.position

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
            leave_point = _np.linalg.solve(leave_dcm,
                                           roller_center_to_platform[[0, 2]])

            # "unwrapped angle"
            unwrapped = _np.arctan2(leave_point[1], leave_point[0])

            cable_leave_points.append(leave_point[0:num_lin])

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
                                 fanchor.linear.position - (
                                 ppos + prot.dot(
                                 panchor.linear.position))))
            # direction = direction[0:num_lin] / length_workspace
            directions.append(direction[0:num_lin] / length_workspace)

        # turn everything into numpy arrays
        lengths = _np.asarray(lengths)
        directions = _np.asarray(directions)
        swivel = _np.asarray(swivel)
        wrap = _np.asarray(wrap)
        leave_points = _np.asarray(cable_leave_points)

        return _algorithm.Result(self,
                                 robot,
                                 pose,
                                 lengths=lengths,
                                 directions=directions,
                                 swivel=swivel,
                                 wrap=wrap,
                                 leave_points=leave_points)
