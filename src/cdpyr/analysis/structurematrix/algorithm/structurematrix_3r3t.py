from typing import Optional

import numpy as np_

from cdpyr.analysis.structurematrix import calculator as _structurematrix
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import platform as _platform
from cdpyr.typing import Matrix


def evaluate(calculator: '_structurematrix.Calculator',
             platform: '_platform.Platform',
             uis: Matrix,
             pose: Optional['_pose.Pose'] = None):
    return np_.vstack((
        uis,
        np_.cross(
            pose.angular.dcm.dot(
                platform.bi
            ),
            uis,
            axis=0
        )
    ))
