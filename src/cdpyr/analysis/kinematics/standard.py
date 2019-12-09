import numpy as _np
from scipy import optimize

from cdpyr.analysis.kinematics import kinematics as _algorithm
from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Standard(_algorithm.Algorithm):

    def _forward(self,
                 robot: '_robot.Robot',
                 lengths: Vector,
                 **kwargs) -> '_algorithm.Result':
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

        # scaling of all parameters to increase sensitivity of the optimizer
        scaling = _np.asarray([0.1, 0.1, 0.1, 10.0, 10.0, 10.0, 10.0]) * 10

        # initial directions needed for later returned result
        last_direction = []

        # goal function for the estimator
        def goal_function(x):
            # remove scaling
            x = x / scaling

            # estimate position
            pos = x[0:3]
            # estimated rotation matrix from quaternions
            dcm = _angular.Angular(quaternion=x[3:7]).dcm

            # solve the inverse kinematics vector loop
            directions = self._vector_loop(pos,
                                           dcm,
                                           frame_anchors,
                                           platform_anchors)

            # strip additional spatial dimensions
            directions = directions[0:platform.motion_pattern.dof_translation,
                         :]

            last_direction.insert(0, directions)

            # cable lengths
            estimated_lengths = _np.linalg.norm(directions, axis=0)

            # return error as || l - l_in || ^ 2
            return _np.linalg.norm(estimated_lengths - lengths) ** 2

        # initial pose estimate given by user?
        initial_estimate = kwargs.get('x0', None)
        # no initial pose estimate given, so calculate one based on Schmidt.2016
        if initial_estimate is None:
            # initial_estimate = self._pose_estimate(robot, lengths)
            initial_estimate = _np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

        # introduce scaling
        initial_estimate *= scaling

        # bounds of estimation
        bounds = optimize.Bounds([-_np.inf, -_np.inf, -_np.inf, -1, -1, -1, -1],
                                 [_np.inf, _np.inf, _np.inf, 1, 1, 1, 1])

        # minimization method to use
        method: str = kwargs.get('method', 'COBYLA')

        # tolerances on step size, residual size, and constraint residual size
        xtol, ftol, gtol = 1e-14, 1e-12, 1e-14

        # default options of all supported minimization methods
        method_option_defaults = {
                'Nelder-Mead': {
                        'xtol': xtol,
                        'ftol': ftol,
                },
                'Powell':      {
                        'xtol': xtol,
                        'ftol': ftol,
                },
                'CG':          {
                        'gtol': gtol,
                },
                'BFGS':        {
                        'gtol': gtol,
                },
                'Newton-CG':   {
                        'xtol': xtol,
                },
                'L-BFGS-B':    {
                        'ftol':  ftol,
                        'gtol':  gtol,
                        'factr': 1e4,
                },
                'TNC':         {
                        'xtol': xtol,
                        'ftol': ftol,
                        'gtol': gtol,
                },
                'COBYLA':      {
                        'tol': ftol,
                },
                'SLSQP':       {
                        'ftol': ftol,
                },
                'dogleg':      {
                        'gtol': gtol,
                },
                'trust-ncg':   {
                        'gtol': gtol,
                },
        }

        method_options = {'maxiter': 7 * 314, 'disp': False}
        try:
            method_options += method_option_defaults[method.lower()]
        except (KeyError, TypeError):
            pass

        # estimate the pose
        result: optimize.OptimizeResult
        result = optimize.minimize(goal_function,
                                   initial_estimate,
                                   # bounds=bounds,
                                   options=method_options)

        # check for convergence
        try:
            if result.success is not True:
                raise ArithmeticError(
                        f'Optimizer did not exit successfully. Last message '
                        f'was '
                        f'{result.message}')
        except ArithmeticError as ArithmeticE:
            raise ValueError(
                    'Unable to solve the standard forward kinematics for the '
                    'given cable lengths. Please check if your inputs are '
                    'correct and then run again. You may also pass additional '
                    'arguments to the underlying optimization method.') from \
                ArithmeticE
        else:
            final = result.x / scaling

            pose = _pose.Pose(
                    final[0:3],
                    angular=_angular.Angular(quaternion=final[3:7])
            )

            return _algorithm.Result(self, robot, pose, lengths=lengths,
                                     directions=last_direction[0])

    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> '_algorithm.Result':
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
        directions = directions / lengths

        # to avoid divisions by zero yielding `NaN`, we will set all unit
        # vectors to zero where the cable length is zero. technically,
        # this case is not well-defined, however, from the standard
        # kinematics algorithm_old there is no force transmitted, so ui == 0
        # in this case
        directions[:, _np.isclose(lengths, 0)] = 0

        return _algorithm.Result(self, robot, pose, lengths=lengths,
                                 directions=directions, swivel=swivel)

    def _vector_loop(self,
                     position: Matrix,
                     dcm: Matrix,
                     frame_anchor: Matrix,
                     platform_anchor: Matrix):
        return frame_anchor - (
                position[:, _np.newaxis] + dcm.dot(platform_anchor)
        )

    def _pose_estimate(self, robot: '_robot.Robot', lengths: Vector):
        # consistent arguments
        lengths = _np.asarray(lengths)

        # initialize estimated initial position
        estimate = _np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

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


__all__ = [
        'Standard',
]
