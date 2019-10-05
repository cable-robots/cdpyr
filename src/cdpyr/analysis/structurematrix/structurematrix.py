from typing import Optional, Sequence

from magic_repr import make_repr

from cdpyr.analysis import kinematics as _kinematics
from cdpyr.analysis.kinematics import _algorithm as _kinematicsalgorithm
from cdpyr.motion import (
    pose as _pose,
)
from cdpyr.robot import robot as _robot


class StructureMatrix(object):

    def __call__(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose',
                 kinematics: Optional['_kinematicsalgorithm.Algorithm'] = None
                 ):
        # and make sure we are dealing with a sequence of poses
        poses = pose if isinstance(pose, Sequence) else [pose]

        # ensure we have just as many uis and poses as platforms
        if len(robot.platforms) != len(poses):
            raise ValueError(
                'number of pose must match number of robot platforms.')

        # solve the inverse kinematics as given by the user
        if kinematics is None:
            kinematics = _kinematics.Kinematics.STANDARD
        _, uis, _ = kinematics.backward(robot, pose)

        # init return value
        structurematrices = []

        # loop over each platform and calculate its structure matrix
        for idx, platform in enumerate(robot.platforms):
            # get platform's pose
            pose = poses[idx]
            # get platform's cable unit direction vectors
            ui = uis[idx]

            # calculate the platforms structure matrix
            structurematrices.append(
                self._resolve_structure_matrix(platform, pose, ui))
            # structurematrices.append(self.MAPPING[
            # platform.motionpattern.name](pose, ui))

    def _resolve_structure_matrix(self, platform, pose, ui):
        pass


StructureMatrix.__repr__ = make_repr()

__all__ = [
    'StructureMatrix'
]
