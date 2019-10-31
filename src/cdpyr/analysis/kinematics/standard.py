import numpy as _np

from cdpyr.analysis.kinematics import algorithm as _algorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Standard(_algorithm.Algorithm):

    def _forward(self,
                 robot: '_robot.Robot',
                 joints: Vector,
                 **kwargs) -> dict:
        raise NotImplementedError()

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
        directions = directions[0:platform.motionpattern.dof_translation, :]

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


__all__ = [
    'Standard',
]
