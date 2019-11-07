import numpy as _np
from scipy import optimize

from cdpyr.analysis.kinematics import algorithm as _algorithm
from cdpyr.motion.pose import generator as _pose_generator, pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Standard(_algorithm.Algorithm):

    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Vector,
                 **kwargs) -> dict:
        # consistent arguments
        joints = _np.asarray(joints)

        # quicker and shorter access to platform object
        platform = robot.platforms[0]

        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray(
            [anchor.position for anchor in kcs.frame_anchor]).T
        platform_anchors = _np.asarray(
            [anchor.position for anchor in kcs.platform_anchor]).T

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
            dcm = _pose_generator.from_quaternion(x[3:7], False)

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
            estimated_joints = _np.linalg.norm(directions, axis=0)

            # return error as || l - l_in || ^ 2
            return _np.linalg.norm(estimated_joints - joints) ** 2

        # initial pose estimate given by user?
        initial_estimate = kwargs.get('x0', None)
        # no initial pose estimate given, so calculate one based on Schmidt.2016
        if initial_estimate is None:
            initial_estimate = self._pose_estimate(robot, joints)
            initial_estimate = _np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

        # introduce scaling
        initial_estimate *= scaling

        # bounds of estimation
        bounds = optimize.Bounds([-_np.inf, -_np.inf, -_np.inf, -1, -1, -1, -1],
                                 [_np.inf, _np.inf, _np.inf, 1, 1, 1, 1])

        # minimization method to use
        method: str = kwargs.get('method', 'COBYLA')

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
                    f'Optimizer did not exit successfully. Last message was '
                    f'{result.message}')
        except ArithmeticError as ArithmeticE:
            raise ValueError(
                'Unable to solve the standard forward kinematics for the '
                'given joints. Please check if your inputs are correct and '
                'then run again. You may also pass additional arguments to '
                'the underlying optimization method.') from ArithmeticE
        else:
            x = result.x / scaling

            return {
                'pose':       _pose.Pose((
                    x[0:3],
                    _pose_generator.from_quaternion(x[3:7])
                )),
                'joints':     joints,
                'directions': last_direction[0]
            }

    def _backward(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs) -> dict:
        # quicker and shorter access to platform object
        platform = robot.platforms[0]

        # get platform position
        pos, rot = pose.position
        # kinematic chains of the platform
        kcs = robot.kinematic_chains.with_platform(platform)
        # get frame anchors and platform anchors
        frame_anchors = _np.asarray(
            [anchor.position for anchor in kcs.frame_anchor]).T
        platform_anchors = _np.asarray(
            [anchor.position for anchor in kcs.platform_anchor]).T

        # cable directions
        directions = self._vector_loop(pos,
                                       rot,
                                       frame_anchors,
                                       platform_anchors)

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

        return {
            'pose':       pose,
            'joints':     lengths,
            'directions': directions
        }

    def _vector_loop(self,
                     position: Matrix,
                     dcm: Matrix,
                     frame_anchor: Matrix,
                     platform_anchor: Matrix):
        return frame_anchor - (
            position[:, _np.newaxis] + dcm.dot(platform_anchor)
        )

    def _pose_estimate(self, robot: '_robot.Robot', joints: Vector):
        # consistent arguments
        joints = _np.asarray(joints)

        # calculate using the kinematic chains
        kcs = robot.kinematic_chains

        # initialize estimated initial position
        estimate = _np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

        frame_anchors = _np.vstack(
            [anchor.linear.position for anchor in kcs.frame_anchor]).T[
                        0:robot.platforms[0].dof_translation, :]
        platform_anchors = _np.vstack(
            [anchor.linear.position for anchor in kcs.platform_anchor]).T[
                           0:robot.platforms[0].dof_translation, :]

        radius_low = _np.max(frame_anchors - (joints + _np.linalg.norm(
            platform_anchors, axis=0))[_np.newaxis, :], axis=1)
        radius_high = _np.min(frame_anchors + (joints + _np.linalg.norm(
            platform_anchors, axis=0))[_np.newaxis, :], axis=1)

        # use center of bounding box as initial estimate
        estimate[0:robot.platforms[0].dof_translation] = 0.5 * (
                radius_high + radius_low)

        return estimate


__all__ = [
    'Standard',
]
