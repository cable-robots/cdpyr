from typing import Sequence, Union

from magic_repr import make_repr

from cdpyr.analysis.structurematrix.algorithm import (
    StructureMatrix1R2T as _StructureMatrix1R2T,
    StructureMatrix1T as _StructureMatrix1T,
    StructureMatrix2R3T as _StructureMatrix2R3T,
    StructureMatrix2T as _StructureMatrix2T,
    StructureMatrix3R3T as _StructureMatrix3R3T,
    StructureMatrix3T as _StructureMatrix3T,
)
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix


class StructureMatrix(object):
    # mapping of literal motion pattern name to the structure matrix class
    # for the motion pattern
    _MAPPING = {
        _motionpattern.Motionpattern.MP_1T.name:   _StructureMatrix1T(),
        _motionpattern.Motionpattern.MP_2T.name:   _StructureMatrix2T(),
        _motionpattern.Motionpattern.MP_3T.name:   _StructureMatrix3T(),
        _motionpattern.Motionpattern.MP_1R2T.name: _StructureMatrix1R2T(),
        _motionpattern.Motionpattern.MP_2R3T.name: _StructureMatrix2R3T(),
        _motionpattern.Motionpattern.MP_3R3T.name: _StructureMatrix3R3T()
    }

    @classmethod
    def evaluate(cls,
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
                                     ].evaluate(platform, uis[idx], pose[idx])
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
        return self.evaluate(robot, uis, pose)

    def _resolve_structure_matrix(self, platform, pose, ui):
        pass


StructureMatrix.__repr__ = make_repr()

__all__ = [
    'StructureMatrix'
]
