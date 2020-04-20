from __future__ import annotations

__all__ = [
        'Interference',
]
__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

import numpy as _np

from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.exceptions import InvalidPoseException
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot


class Interference(_criterion.Criterion):
    kinematics: _kinematics.Algorithm

    def __init__(self, kinematics: _kinematics.Algorithm, **kwargs):
        super().__init__(**kwargs)
        self.kinematics = kinematics

    def _evaluate(self,
                  robot: _robot.Robot,
                  pose: _pose.Pose,
                  **kwargs):
        # solve the inverse kinematics
        kinematics_solution = self.kinematics.backward(robot, pose)

        # get all leave points
        leave_points = kinematics_solution.leave_points

        # position and orientation of the robot
        pos, rot = pose.position

        # local sorted platform anchors
        platform_anchors = _np.vstack([robot.platforms[kc.platform].anchors[
                                           kc.platform_anchor].linear.position
                                       for kc in robot.kinematic_chains]).T

        # global sorted platform anchors
        platform_anchors = pos[:, None] + rot.dot(platform_anchors)

        # build a list of line segments composed of [leave, platform]
        line_segments = list(zip(leave_points.T, platform_anchors.T))

        # pick one cable to test against the others
        for this_idx in range(len(line_segments)):
            this_segment = line_segments[this_idx]
            # just check the remaining cables
            for that_idx in range(this_idx + 1, len(line_segments)):
                that_segment = line_segments[that_idx]
                # build array of segments
                segments = _np.vstack((this_segment[1] - this_segment[0],
                                       that_segment[0] - that_segment[1])).T
                # calculate common point
                common = that_segment[0] - this_segment[0]
                # solve to see if there's a common value for lambda
                try:
                    lbda, res, rank, s = _np.linalg.lstsq(segments, common,
                                                          rcond=None)
                    print(lbda)

                    if _np.logical_and(0 <= lbda, lbda <= 1).all():
                        raise InvalidPoseException(
                                f'invalid pose found. cables of kinematic '
                                f'chains {this_idx} and {that_idx} collide')
                except _np.linalg.LinAlgError as e:
                    # valid pose, just move on
                    pass
