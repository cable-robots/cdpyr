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
from cdpyr.robot import kinematicchain as _kinematic_chain, robot as _robot
from cdpyr.typing import Vector


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
                 anchor_index in kcs.frame_anchor])
        platform_anchors = _np.asarray(
                [platform.anchors[anchor_index].linear.position for anchor_index
                 in kcs.platform_anchor])

        # initial directions needed for later returned result
        last_direction = []

        # goal function for the estimator
        def goal_function(x: Vector,
                          robot_: _robot.Robot,
                          xpose_: _pose.Pose,
                          *args,
                          **kwargs):
            # position estimate
            xpose_.linear.position = x[0:3]
            # euler angle estimate to rotation matrix
            xpose_.angular = _angular.Angular(sequence='xyz', euler=x[3:6])

            # solve the vector loop and obtain solution
            estim_lengths, directions, _ = self._vector_loop(robot_, xpose_)

            # number of linear degrees of freedom
            num_linear, _ = robot.num_dimensions
            # strip additional spatial dimensions
            directions = directions[:, 0:num_linear]

            # store last direction so we have it later
            last_direction.insert(0, directions)

            # return error as (l^2 - l(x)^2)
            return lengths ** 2 - estim_lengths ** 2

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

        # # default keyword arguments to `least_squares`
        # defaults = {
        #         'method':  method,
        #         'ftol':    ftol,
        #         'xtol':    xtol,
        #         'gtol':    gtol,
        #         'x_scale': x_scale,
        #         'jac':     '3-point',
        #         'args':    (
        #                 frame_anchors,
        #                 platform_anchors,
        #         ),
        #         'kwargs':  {
        #                 'ai': frame_anchors,
        #                 'bi': platform_anchors
        #         },
        # }
        # # only add `bounds` if the solver is not `lm` (levenberg-marquardt)
        # if method != 'lm':
        #     defaults['bounds'] = bounds
        # # update with user-supplied kwargs
        # defaults.update(kwargs)

        # a pose estimate
        x_pose = _pose.ZeroPose

        # estimate pose
        result: optimize.OptimizeResult
        result = optimize.least_squares(goal_function,
                                        initial_estimate,
                                        args=(robot, x_pose),
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

            # and return estimated result
            return _algorithm.Result(self,
                                     robot,
                                     x_pose,
                                     lengths=lengths,
                                     directions=last_direction[0],
                                     leave_points=frame_anchors)

    def _backward(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs) -> _algorithm.Result:
        # solve the vector loop and obtain solution
        lengths, directions, leaves = self._vector_loop(robot, pose)

        # cable swivel angles
        swivel = _np.arctan2(-directions[:, 1], -directions[:, 0])

        # number of linear degrees of freedom
        num_linear, _ = robot.num_dimensions
        # strip additional spatial dimensions
        directions = directions[:, 0:num_linear]

        # return algorithm result object
        return _algorithm.Result(self,
                                 robot,
                                 pose,
                                 lengths=lengths,
                                 directions=directions,
                                 swivel=swivel,
                                 leave_points=leaves)

    def _vector_loop(self, robot: _robot.Robot, pose: _pose.Pose):
        # number of linear degrees of freedom
        num_linear, _ = robot.num_dimensions
        # cable vector
        cables = [] #_np.zeros((num_kinchains, num_linear))
        # cable leave points
        leaves = [] # _np.zeros((num_kinchains, num_linear))

        # loop over each kinematic chain
        kc: _kinematic_chain.KinematicChain
        for idxkc, kc in enumerate(robot.kinematic_chains):
            # extract frame anchor, platform, and platform anchor
            fanchor = robot.frame.anchors[kc.frame_anchor].linear.position
            platform = robot.platforms[kc.platform]
            panchor = platform.anchors[kc.platform_anchor].linear.position

            # store frame anchor point as cable leave point
            leaves.append(fanchor)

            # read platform position and orientation
            pos, rot = pose.position

            # write vector loop
            cables.append(fanchor - (pos + rot.dot(panchor)))

        # ensure cables is a numpy array from this point on
        cables = _np.asarray(cables)

        # cable lengths
        lengths = _np.linalg.norm(cables, axis=1)

        # determine cable directions and set any division by zero to 0
        directions = cables / lengths[: , None]
        directions[_np.isclose(lengths, 0), :] = 0

        # return lengths li, directions ui, and leaves ai
        return lengths, directions, _np.asarray(leaves)

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
