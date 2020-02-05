from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

import numpy as _np

import cdpyr.numpy.linalg
from cdpyr.analysis import result as _result
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(ABC):

    def __init__(self):
        pass

    def forward(self,
                robot: _robot.Robot,
                joints: Matrix,
                **kwargs) -> Result:
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Kinematics are currently not implemented for robots with '
                    'more than one platform.'
            )

        return self._forward(robot, joints, **kwargs)

    direct = forward

    def backward(self,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 **kwargs) -> Result:
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Kinematics are currently not implemented for robots with '
                    'more than one platform.'
            )

        return self._backward(robot, pose, **kwargs)

    inverse = backward

    @abstractmethod
    def _forward(self,
                 robot: _robot.Robot,
                 joints: Matrix,
                 **kwargs) -> Result:
        raise NotImplementedError()

    @abstractmethod
    def _backward(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs) -> Result:
        raise NotImplementedError()


class Result(_result.PoseResult, _result.RobotResult, _result.PlottableResult):
    """

    """

    """
    Algorithm used for calculation of the kinematics result
    """
    _algorithm: 'Algorithm'

    """
    `(NT, M)` array of unit cable direction vectors
    """
    _directions: Matrix

    """
    `(NT,M)` array of cached cable leave points. Cable leave points are the
    spatial points where the cable leaves the pulley or frame and enters the
    workspace.
    """
    _leave_points: Matrix

    """
    `(2, M)` array where each column consists of `[workspace, pulley]` lengths
    """
    _lengths: Matrix

    """
    `(NT,M,100)` array cached cable shape over 100 steps (99 on the pulley,
    if pulleys are available, and 1 step between the cable leave point and
    the platform
    """
    _cable_shapes: Matrix

    """
    `(M,)` of swivel angles of each cable frame
    """
    _swivel: Vector

    """
    `(M,)` of wrap angles of each pulley
    """
    _wrap: Vector

    def __init__(self,
                 algorithm: Algorithm,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 lengths: Union[Vector, Matrix],
                 directions: Matrix,
                 swivel: Vector = None,
                 wrap: Vector = None,
                 leave_points: Matrix = None,
                 **kwargs):
        super().__init__(pose, robot=robot, **kwargs)
        self._algorithm = algorithm
        lengths = _np.asarray(lengths)
        self._lengths = lengths if lengths.ndim == 2 else lengths[None, :]
        self._directions = _np.asarray(directions)
        self._swivel = _np.asarray(swivel) if swivel is not None else None
        self._wrap = _np.asarray(wrap) if wrap is not None else None
        self._leave_points = leave_points
        self._cable_shapes = None

    @property
    def directions(self):
        return self._directions

    @property
    def cable_shapes(self):
        if self._cable_shapes is None:
            # number of discretization steps for the wrapped part
            num = 100

            # storing all forms in here as
            shapes = _np.zeros((3, self._robot.num_kinematic_chains, num))

            # unit vector along the first axis in 3D
            evec_x = cdpyr.numpy.linalg.evec3_1()
            eye = _np.eye(3)

            # loop over each kinematic chain
            for index_chain, chain in enumerate(self._robot.kinematic_chains):
                # get frame anchor, platform, platform anchor, and cable
                frame_anchor = self._robot.frame.anchors[chain.frame_anchor]
                platform = self._robot.platforms[chain.platform]
                platform_anchor = platform.anchors[chain.platform_anchor]
                cable = self._robot.cables[chain.cable]

                # get platform position and orientation
                platform_pos, platform_dcm = self._pose.position

                # absolute frame anchor coordinates
                frame_anchor_coordinates = frame_anchor.linear.position

                # transform platform anchor into its world coordinates
                platform_anchor_coords = platform_pos + platform_dcm.dot(
                        platform_anchor.linear.position)

                shapes[:, index_chain, 0:num - 1] = frame_anchor_coordinates[:,
                                                    None]

                # first, the part on the drum
                try:
                    # we discretize with a step of 2deg (should be fine)
                    linspace_wrap = _np.linspace(0, self._wrap[index_chain],
                                                 num=num - 1, endpoint=True)

                    # calculate shape on the pulley
                    pulley_shape = _np.asarray([frame_anchor.pulley.radius * (
                            eye - transform.dcm).dot(evec_x) for transform in
                                                _angular.Angular.rotation_y(
                                                        linspace_wrap)]).T

                    # pre-calculate and pre-gather some rotation matrices
                    cable_dcm = _angular.Angular.rotation_z(
                            self._swivel[index_chain]).dcm
                    pulley_dcm = frame_anchor.pulley.dcm
                    frame_dcm = frame_anchor.dcm

                    # transform coordinates back into world coordinates and
                    # store
                    shapes[:, index_chain, 0:num - 1] += frame_dcm.dot(
                            pulley_dcm.dot(cable_dcm.dot(pulley_shape)))
                except (TypeError, KeyError, ValueError) as e:
                    pass

            # the last step will be to close the loop from the cable leave point
            # to the platform anchor which we will append as a simple last point
            shapes[:, :, -1] = shapes[:, :, -2] \
                               - self.workspace_length[None,
                                 :] * self._directions
            # cache result
            self._cable_shapes = shapes

        return self._cable_shapes

    @property
    def joints(self):
        return _np.sum(self._lengths, axis=0)

    @property
    def leave_points(self):
        """
        Return the cable leave point i.e., the point where the cable leaves
        the pulley and enters the workspace. If the robot uses pulleys,
        the point will be on the pulley, otherwise the point will coincide
        with the frame anchor position

        Returns
        -------
        coordinates : Matrix
            (3,M) matrix of `(3,)` vectors for `M` kinematic chains of  the
            robot.
        """

        if self._leave_points is None:
            # init output
            points = _np.zeros((3, self._robot.num_kinematic_chains))

            # unit vector along the first axis in 3D
            evec_x = cdpyr.numpy.linalg.evec3_1()

            # loop over each kinematic chain
            for index_chain, chain in enumerate(self._robot.kinematic_chains):
                # get frame anchor, platform, platform anchor, and cable
                frame_anchor = self._robot.frame.anchors[chain.frame_anchor]
                platform = self._robot.platforms[chain.platform]
                # platform_anchor = platform.anchors[chain.platform_anchor]
                # cable = self._robot.cables[chain.cable]

                # calculate corrected cable leave point
                points[:, index_chain] = frame_anchor.linear.position
                try:
                    # pre-calculate wrap and swivel rotation matrix
                    wrap_dcm = _angular.Angular.rotation_y(
                            self._wrap[index_chain]).dcm
                    swivel_dcm = _angular.Angular.rotation_z(
                            self._swivel[index_chain]).dcm
                    pulley_dcm = frame_anchor.pulley.dcm
                    anchor_dcm = frame_anchor.dcm

                    # append the correction along the pulley to the original
                    # frame anchor position
                    points[:, index_chain] += anchor_dcm.dot(pulley_dcm.dot(
                            swivel_dcm.dot(((_np.eye(3) - wrap_dcm).dot(
                                    frame_anchor.pulley.radius * evec_x)))))
                except (TypeError, ValueError, KeyError) as e:
                    pass

            self._leave_points = points

        return self._leave_points

    @property
    def lengths(self):
        return self.joints

    @property
    def swivel_angles(self):
        return self._swivel

    @property
    def workspace_length(self):
        return self._lengths[0, :]

    @property
    def wrapped_length(self):
        try:
            return self._lengths[1, :]
        except IndexError:
            return None

    @property
    def wrap_angles(self):
        return self._wrap


__all__ = [
        'Algorithm',
        'Result',
]
