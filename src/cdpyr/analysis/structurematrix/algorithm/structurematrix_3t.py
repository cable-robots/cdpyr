from typing import Optional

from cdpyr.analysis.structurematrix import structurematrix as _structurematrix
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def evaluate(calculator: '_structurematrix.Calculator',
             platform: '_platform.Platform',
             uis: Matrix,
             pose: Optional['_pose.Pose'] = None):
    return uis[0:3, :]
