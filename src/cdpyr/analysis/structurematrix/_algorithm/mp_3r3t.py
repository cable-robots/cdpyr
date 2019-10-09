from typing import Sequence

from cdpyr.analysis.structurematrix._algorithm.algorithm import Algorithm
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Vector


class MP_3R3T(Algorithm):

    @staticmethod
    def _calculate(platform: '_platform.Platform', pose: '_pose.Pose',
                   uis: Sequence[Vector]):
        pass
        # noc = len(uis)
        # sm = np_.zeros([6, noc])
        # _, R = pose.position
        #
        # for ic in range(0, noc):
        #     sm[0:4,ic] = uis[ic]
        #     sm[4:7],ic] = np_.cross(np_.dot(R, platform.bi[ic].))
