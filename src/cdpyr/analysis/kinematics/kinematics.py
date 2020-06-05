from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Algorithm',
        'Result',
]

from abc import ABC, abstractmethod
from typing import Union

import numpy as _np
from magic_repr import make_repr
from scipy import optimize

import cdpyr.numpy.linalg
from cdpyr.analysis import result as _result
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class Algorithm(ABC):

    def __init__(self, **kwargs):
        self._forward_last_direction = None

    @abstractmethod
    def _vector_loop(self,
                     robot: _robot.Robot,
                     pose: _pose.Pose,
                     *args,
                     **kwargs):
        raise NotImplementedError()

    def backward(self,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 **kwargs) -> Result:
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Kinematics are currently not implemented for robots with '
                    'more than one platform.'
            )
        # solve the vector loop and obtain solution
        lengths, directions, leaves, swivel, *rem = self._vector_loop(robot,
                                                                      pose,
                                                                      **kwargs)
        try:
            wrap, *rem = rem
        except ValueError:
            wrap = None

        # number of linear degrees of freedom
        num_linear, _ = robot.num_dimensionality
        # strip additional spatial dimensions
        directions = directions[:, 0:num_linear]

        # return algorithm result object
        return Result(self,
                      robot,
                      pose,
                      lengths=lengths,
                      directions=directions,
                      leave_points=leaves,
                      swivel=swivel,
                      wrap=wrap)

    def forward(self,
                robot: _robot.Robot,
                joints: Matrix,
                **kwargs) -> Result:
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Kinematics are currently not implemented for robots with '
                    'more than one platform.'
            )

        # for now, this is the inner-loop code for the first platform
        index_platform = 0

        # consistent arguments
        joints = _np.asarray(joints)

        # quicker and shorter access to platform object
        platform = robot.platforms[index_platform]

        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(index_platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray(
                [robot.frame.anchors[anchor_index].linear.position for
                 anchor_index in kcs.frame_anchor])

        # initial directions needed for later returned result
        last_direction = []

        # initial pose estimate given by user?
        initial_estimate = kwargs.pop('x0', None)
        # no initial pose estimate given, so calculate one based on Schmidt.2016
        if initial_estimate is None:
            initial_estimate = self._pose_estimate(robot, joints)

        # a pose estimate
        x_pose = _pose.ZeroPose

        # extract forward kinematics goal function from the kwargs, or default
        # to our own implementation
        goal_function = kwargs.pop('goal_function', self._forward_goal_function)

        # estimate pose
        result: optimize.OptimizeResult
        result = optimize.least_squares(goal_function,
                                        initial_estimate,
                                        args=(robot, x_pose, joints),
                                        **kwargs)

        # check for convergence
        try:
            if result.success is not True:
                raise ArithmeticError(
                        f'Optimizer did not exit successfully. Last message '
                        f'was {result.message}')
        except ArithmeticError as ArithmeticE:
            raise ValueError(
                    'Unable to solve the standard forward kinematics for the '
                    'given cable lengths. Please check if your inputs are '
                    'correct and then run again. You may also pass additional '
                    'arguments to the underlying optimization method.') from \
                ArithmeticE
        else:
            # get last value
            final = result.x
            # make sure rotation is limited to [0, 2*pi)
            final[3:6] = _np.fmod(final[3:6], 2 * _np.pi)

            # populate values of estimated pose
            x_pose.linear.position = final[0:3]
            x_pose.angular = _angular.Angular(sequence='xyz', euler=final[3:6])

            # get and reset last forward direction
            last_direction = self._forward_last_direction
            self._forward_last_direction = None

            # and return estimated result
            return Result(self,
                          robot,
                          x_pose,
                          lengths=joints,
                          directions=last_direction,
                          leave_points=frame_anchors)

    direct = forward

    inverse = backward

    def _pose_estimate(self, robot: _robot.Robot, lengths: Vector):
        # consistent arguments
        lengths = _np.asarray(lengths)

        # initialize estimated initial position
        estimate = _np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # for now, this is the inner-loop code for the first platform
        index_platform = 0

        # quicker and shorter access to platform object
        platform = robot.platforms[index_platform]

        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(index_platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray([anchor.position for idx, anchor in
                                     enumerate(robot.frame.anchors) if
                                     idx in kcs.frame_anchor]).T
        platform_anchors = _np.asarray([anchor.position for idx, anchor in
                                        enumerate(platform.anchors) if
                                        idx in kcs.platform_anchor]).T

        radius_low = _np.max(frame_anchors - (lengths + _np.linalg.norm(
                platform_anchors, axis=0))[_np.newaxis, :], axis=1)
        radius_high = _np.min(frame_anchors + (lengths + _np.linalg.norm(
                platform_anchors, axis=0))[_np.newaxis, :], axis=1)

        # build index slicer to push values into correct entries
        platform_slice = slice(0,
                               robot.platforms[index_platform].dof_translation)

        # use center of bounding box as initial estimate
        estimate[platform_slice] = (0.5 * (radius_high + radius_low))[
            platform_slice]

        return estimate

    def _forward_goal_function(self,
                               x: Vector,
                               robot: _robot.Robot,
                               pose: _pose.Pose,
                               joints: Vector,
                               *args,
                               **kwargs):
        # position estimate
        pose.linear.position = x[0:3]
        # euler angle estimate to rotation matrix
        pose.angular = _angular.Angular(sequence='xyz', euler=x[3:6])

        # solve the vector loop and obtain solution
        estim_lengths, directions, *_ = self._vector_loop(robot, pose)
        estim_lengths = _np.sum(estim_lengths, axis=1)

        # number of linear degrees of freedom
        num_linear, _ = robot.num_dimensionality
        # strip additional spatial dimensions
        directions = directions[:, 0:num_linear]

        # store last direction so we have it later
        self._forward_last_direction = directions

        # return error as (l^2 - l(x)^2)
        return joints ** 2 - estim_lengths ** 2

    __repr__ = make_repr()


class Result(_result.PoseResult, _result.RobotResult, _result.PlottableResult):
    """

    """

    _algorithm: Algorithm
    """
    Algorithm used for calculation of the kinematics result
    """

    _directions: Matrix
    """
    `(NT, M)` array of unit cable direction vectors
    """

    _leave_points: Matrix
    """
    `(NT,M)` array of cached cable leave points. Cable leave points are the
    spatial points where the cable leaves the pulley or frame and enters the
    workspace.
    """

    _lengths: Matrix
    """
    `(2, M)` array where each column consists of `[workspace, pulley]` lengths
    """

    _cable_shapes: Matrix
    """
    `(NT,M,100)` array cached cable shape over 100 steps (99 on the pulley,
    if pulleys are available, and 1 step between the cable leave point and
    the platform
    """

    _swivel: Vector
    """
    `(M,)` of swivel angles of each cable frame
    """

    _wrap: Vector
    """
    `(M,)` of wrap angles of each pulley
    """

    def __init__(self,
                 algorithm: Algorithm,
                 robot: _robot.Robot,
                 pose: _pose.Pose,
                 lengths: Union[Vector, Matrix],
                 directions: Matrix,
                 leave_points: Matrix = None,
                 swivel: Vector = None,
                 wrap: Vector = None,
                 **kwargs):
        super().__init__(pose=pose, robot=robot, **kwargs)
        self._algorithm = algorithm
        lengths = _np.asarray(lengths)
        self._lengths = lengths if lengths.ndim == 2 else lengths[:, None]
        self._directions = _np.asarray(directions)
        self._leave_points = leave_points
        self._swivel = _np.asarray(swivel) if swivel is not None else None
        self._wrap = _np.asarray(wrap) if wrap is not None else None
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
            for idxkc, kc in enumerate(self._robot.kinematic_chains):
                # get frame anchor, platform, platform anchor, and cable
                fanchor = self._robot.frame.anchors[kc.frame_anchor]
                platform = self._robot.platforms[kc.platform]
                panchor = platform.anchors[kc.platform_anchor]
                # cable = self._robot.cables[kc.cable]

                # get platform position and orientation
                platform_pos, platform_dcm = self._pose.position

                # absolute frame anchor coordinates
                frame_anchor_coordinates = fanchor.linear.position

                # # transform platform anchor into its world coordinates
                # platform_anchor_coords = platform_pos \
                #                          + platform_dcm.dot(
                #                          panchor.linear.position)

                shapes[:, idxkc, 0:num - 1] = frame_anchor_coordinates[:, None]

                # first, the part on the drum
                try:
                    # we discretize with a step of 2deg (should be fine)
                    linspace_wrap = _np.linspace(0,
                                                 self._wrap[idxkc],
                                                 num=num - 1,
                                                 endpoint=True)

                    # calculate shape on the pulley
                    pulley_shape = _np.asarray([
                            fanchor.pulley.radius
                            * (eye - transform.dcm).dot(evec_x)
                            for transform
                            in _angular.Angular.rotation_y(linspace_wrap)]).T

                    # pre-calculate and pre-gather some rotation matrices
                    cable_dcm = _angular.Angular.rotation_z(
                            self._swivel[idxkc]).dcm
                    pulley_dcm = fanchor.pulley.dcm
                    frame_dcm = fanchor.dcm

                    # transform coordinates back into world coordinates and
                    # store
                    shapes[:, idxkc, 0:num - 1] += frame_dcm.dot(
                            pulley_dcm.dot(cable_dcm.dot(pulley_shape)))
                except (TypeError, KeyError, ValueError) as e:
                    pass

            # the last step will be to close the loop from the cable leave point
            # to the platform anchor which we will append as a simple last point
            shapes[:, :, -1] = shapes[:, :, -2] \
                               - self.workspace_length[None, :] \
                               * self._directions
            # cache result
            self._cable_shapes = shapes

        return self._cable_shapes

    @property
    def joints(self):
        return _np.sum(self._lengths, axis=1)

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
                # platform = self._robot.platforms[chain.platform]
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
        return self._lengths[:, 0]

    @property
    def wrapped_length(self):
        try:
            return self._lengths[:, 1]
        except IndexError:
            return None

    @property
    def wrap_angles(self):
        return self._wrap
