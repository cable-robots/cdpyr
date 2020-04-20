from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Standard',
]

import numpy as _np
from scipy import optimize

from cdpyr.analysis.kinematics import kinematics as _algorithm
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class Standard(_algorithm.Algorithm):

    def _forward(self,
                 robot: _robot.Robot,
                 lengths: Vector,
                 **kwargs) -> _algorithm.Result:
        # for now, this is the inner-loop code for the first platform
        index_platform = 0

        # consistent arguments
        lengths = _np.asarray(lengths)

        # quicker and shorter access to platform object
        platform = robot.platforms[index_platform]

        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(index_platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray(
                [robot.frame.anchors[anchor_index].linear.position for
                 anchor_index in kcs.frame_anchor]).T
        platform_anchors = _np.asarray(
                [platform.anchors[anchor_index].linear.position for anchor_index
                 in kcs.platform_anchor]).T

        # initial directions needed for later returned result
        last_direction = []

        # goal function for the estimator
        def goal_function(x, ai, bi, *args, **kwargs):
            # position estimate
            pos = x[0:3]
            # euler angle estimate to rotation matrix
            dcm = _angular.Angular(sequence='xyz', euler=x[3:6]).dcm

            # solve the inverse kinematics vector loop
            directions = self._vector_loop(pos,
                                           dcm,
                                           ai,
                                           bi)

            # strip additional spatial dimensions
            directions = directions[0:platform.motion_pattern.dof_translation,
                         :]

            last_direction.insert(0, directions)

            # cable lengths
            estimated_lengths = _np.linalg.norm(directions, axis=0)

            # return error as (l^2 - l(x)^2)
            return lengths ** 2 - estimated_lengths ** 2

        # initial pose estimate given by user?
        initial_estimate = kwargs.pop('x0', None)
        # no initial pose estimate given, so calculate one based on Schmidt.2016
        if initial_estimate is None:
            initial_estimate = self._pose_estimate(robot, lengths)

        # scaling of all parameters to increase sensitivity of the optimizer
        x_scale = kwargs.pop('x_scale', None)
        if x_scale is None:
            x_scale = _np.asarray([0.01, 0.01, 0.01, 100.0, 100.0, 100.0])

        # bounds of estimation
        bounds = ([-_np.inf, -_np.inf, -_np.inf,  # [x, y, z]
                   -0.5 * _np.pi, -0.5 * _np.pi, -0.5 * _np.pi],  # [r, p, y]
                  [_np.inf, _np.inf, _np.inf,  # [x, y, z]
                   0.5 * _np.pi, 0.5 * _np.pi, 0.5 * _np.pi])  # [r, p, y]

        # minimization method to use
        method: str = kwargs.pop('method', 'lm')

        # tolerances for solver
        ftol = _np.sqrt(_np.finfo(float).eps) / 1e5
        xtol = _np.sqrt(_np.finfo(float).eps) / 1e5
        gtol = 0.0

        # default keyword arguments to `least_squares`
        defaults = {
                'method':  method,
                'ftol':    ftol,
                'xtol':    xtol,
                'gtol':    gtol,
                'x_scale': x_scale,
                'jac':     '3-point',
                'args':    (
                        frame_anchors,
                        platform_anchors,
                ),
                'kwargs':  {
                        'ai': frame_anchors,
                        'bi': platform_anchors
                },
        }
        # only add `bounds` if the solver is not `lm` (levenberg-marquardt)
        if method != 'lm':
            defaults['bounds'] = bounds
        # update with user-supplied kwargs
        defaults.update(kwargs)

        # estimate pose
        result: optimize.OptimizeResult
        result = optimize.least_squares(goal_function,
                                        initial_estimate,
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
            final = result.x
            final[3:6] = _np.fmod(final[3:6], 2 * _np.pi)

            pose = _pose.Pose(
                    final[0:3],
                    angular=_angular.Angular(sequence='xyz', euler=final[3:6])
            )

            return _algorithm.Result(self, robot, pose, lengths=lengths,
                                     directions=last_direction[0],
                                     leave_points=frame_anchors)

    def _backward(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs) -> _algorithm.Result:
        # for now, this is the inner-loop code for the first platform
        index_platform = 0
        # quicker and shorter access to platform object
        platform = robot.platforms[index_platform]

        # get platform position
        pos, rot = pose.position
        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(index_platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray(
                [robot.frame.anchors[anchor_index].linear.position for
                 anchor_index in kcs.frame_anchor]).T
        platform_anchors = _np.asarray(
                [platform.anchors[anchor_index].linear.position for anchor_index
                 in kcs.platform_anchor]).T

        # cable directions
        directions = self._vector_loop(pos,
                                       rot,
                                       frame_anchors,
                                       platform_anchors)

        # cable swivel angles
        swivel = _np.arctan2(directions[1, :], directions[0, :])

        # strip additional spatial dimensions
        directions = directions[0:platform.motion_pattern.dof_translation, :]

        # cable lengths
        lengths = _np.linalg.norm(directions, axis=0)

        # unit directions
        directions /= lengths

        # to avoid divisions by zero yielding `NaN`, we will set all unit
        # vectors to zero where the cable length is zero. technically,
        # this case is not well-defined, however, from the standard
        # kinematics algorithm_old there is no force transmitted, so ui == 0
        # in this case
        directions[:, _np.isclose(lengths, 0)] = 0

        return _algorithm.Result(self, robot, pose, lengths=lengths,
                                 directions=directions, swivel=swivel,
                                 leave_points=frame_anchors)

    def _vector_loop(self,
                     position: Matrix,
                     dcm: Matrix,
                     frame_anchor: Matrix,
                     platform_anchor: Matrix):
        return frame_anchor - (
                position[:, _np.newaxis] + dcm.dot(platform_anchor)
        )

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
