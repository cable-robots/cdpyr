from typing import Dict, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.analysis.structurematrix.algorithm import (
    structurematrix1r2t as _mp1r2t,
    structurematrix1t as _mp1t,
    structurematrix2r3t as _mp2r3t,
    structurematrix2t as _mp2t,
    structurematrix3r3t as _mp3r3t,
    structurematrix3t as _mp3t,
)
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix


class StructureMatrix(object):
    # mapping of literal motion pattern name to the structure matrix class
    # for the motion pattern
    _MAPPING = {
        _motionpattern.Motionpattern.MP_1T.name:   _mp1t.StructureMatrix1T(),
        _motionpattern.Motionpattern.MP_2T.name:   _mp2t.StructureMatrix2T(),
        _motionpattern.Motionpattern.MP_3T.name:   _mp3t.StructureMatrix3T(),
        _motionpattern.Motionpattern.MP_1R2T.name:
                                                   _mp1r2t.StructureMatrix1R2T(),
        _motionpattern.Motionpattern.MP_2R3T.name:
                                                   _mp2r3t.StructureMatrix2R3T(),
        _motionpattern.Motionpattern.MP_3R3T.name: _mp3r3t.StructureMatrix3R3T()
    }

    @classmethod
    def calculate(cls,
                  robot: '_robot.Robot',
                  uis: Union[Matrix, Sequence[Matrix]],
                  pose: Union['_pose.Pose', Sequence['_pose.Pose']] = None,
                  ):
        # and make sure we are dealing with a sequence of poses
        pose = pose if isinstance(pose, Sequence) else [pose]

        # make uis a list of matrices
        uis = uis if isinstance(uis, Sequence) else [uis]

        # ensure we have just as many uis and poses as platforms
        if robot.num_platforms != len(pose):
            raise ValueError(
                'Expected `{}` to have {} element{}, got {} instead.'.format(
                    'pose',
                    robot.num_platforms,
                    's' if robot.num_platforms > 1 else '',
                    len(pose)
                ))

        # init return value
        structurematrices = []

        # loop over each platform and calculate its structure matrix
        for idx, platform in enumerate(robot.platforms):
            # calculate the platforms structure matrix
            structurematrices.append(cls._MAPPING[
                                         platform.motionpattern.name
                                     ].calculate(platform, uis[idx], pose[idx])
                                     )

        # in case of robots with only one platform, make the return value a
        # standard structure matrix
        return structurematrices[0] \
            if robot.num_platforms == 1 \
            else structurematrices

    def __call__(self,
                 robot: '_robot.Robot',
                 uis: Union[Matrix, Sequence[Matrix]],
                 pose: Union['_pose.Pose', Sequence['_pose.Pose']] = None,
                 ):
        return self.calculate(robot, uis, pose)

    def _resolve_structure_matrix(self, platform, pose, ui):
        pass


StructureMatrix.__repr__ = make_repr()

__all__ = [
    'StructureMatrix'
]
