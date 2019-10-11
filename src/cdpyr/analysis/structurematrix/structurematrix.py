from typing import Sequence, Union

from magic_repr import make_repr

from cdpyr.analysis.structurematrix.algorithm import (
    motionpattern_1r2t as _mp_1r2t,
    motionpattern_1t as _mp_1t,
    motionpattern_2r3t as _mp_2r3t,
    motionpattern_2t as _mp_2t,
    motionpattern_3r3t as _mp_3r3t,
    motionpattern_3t as _mp_3t,
)
# from cdpyr.analysis.kinematics import algorithm as _kinematicsalgorithm
from cdpyr.motion import pose as _pose
from cdpyr.motion.pattern import motionpattern as _motionpattern
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix


class StructureMatrix(object):
    # mapping of literal motion pattern name to the structure matrix class
    # for the motion pattern
    _MAPPING = {
        _motionpattern.Motionpattern.MP_1T.name:   _mp_1t.MotionPattern_1T(),
        _motionpattern.Motionpattern.MP_2T.name:   _mp_2t.MotionPattern_2T(),
        _motionpattern.Motionpattern.MP_3T.name:   _mp_3t.MotionPattern_3T(),
        _motionpattern.Motionpattern.MP_1R2T.name: _mp_1r2t.MotionPattern_1R2T(),
        _motionpattern.Motionpattern.MP_2R3T.name: _mp_2r3t.MotionPattern_2R3T(),
        _motionpattern.Motionpattern.MP_3R3T.name: _mp_3r3t.MotionPattern_3R3T()
    }

    def __call__(self,
                 robot: '_robot.Robot',
                 uis: Union[Matrix, Sequence[Matrix]],
                 pose: Union['_pose.Pose', Sequence['_pose.Pose']],
                 ):
        # and make sure we are dealing with a sequence of poses
        pose = pose if isinstance(pose, Sequence) else [pose]

        # Make a multi
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
            structurematrices.append(self._MAPPING[
                                         platform.motionpattern.name
                                     ](platform, uis[idx], pose[idx])
                                     )

        # in case of robots with only one platform, make the return value a
        # standard structure matrix
        return structurematrices[0] \
            if robot.num_platforms == 1 \
            else structurematrices

    def _resolve_structure_matrix(self, platform, pose, ui):
        pass


StructureMatrix.__repr__ = make_repr()

__all__ = [
    'StructureMatrix'
]
