from typing import Optional, Sequence, Union

from magic_repr import make_repr

from cdpyr.analysis.structurematrix.algorithm import (
    structurematrix_1r2t,
    structurematrix_1t,
    structurematrix_2r3t,
    structurematrix_2t,
    structurematrix_3r3t,
    structurematrix_3t,
)
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix


class StructureMatrix(object):
    _MAPPING: dict

    def __init__(self):
        self._MAPPING = {
            _motionpattern.Motionpattern.MP_1T.name:   structurematrix_1t,
            _motionpattern.Motionpattern.MP_2T.name:   structurematrix_2t,
            _motionpattern.Motionpattern.MP_3T.name:   structurematrix_3t,
            _motionpattern.Motionpattern.MP_1R2T.name: structurematrix_1r2t,
            _motionpattern.Motionpattern.MP_2R3T.name: structurematrix_2r3t,
            _motionpattern.Motionpattern.MP_3R3T.name: structurematrix_3r3t,
        }

    def evaluate(self,
                 robot: '_robot.Robot',
                 uis: Union[Matrix, Sequence[Matrix]],
                 pose: Optional[
                     Union['_pose.Pose', Sequence['_pose.Pose']]] = None,
                 ):
        if robot.num_platforms > 1:
            raise NotImplementedError(
                'Currently, the structure matrix can only be computed for '
                'single-platform cable robots'
            )

        # get pose of only the first platform
        pose = pose[0] if isinstance(pose, Sequence) else pose

        # get uis of only the first platform
        uis = uis[0] if isinstance(uis, Sequence) else uis

        # TODO implement here the logic to return the extended structure
        #  matrix for multi-platform CDPRs

        # calculate the platforms structure matrix
        return self._MAPPING[robot.platforms[0].motionpattern.name].evaluate(
            self,
            robot.platforms[0],
            uis,
            pose)


StructureMatrix.__repr__ = make_repr()

__all__ = [
    'StructureMatrix'
]
