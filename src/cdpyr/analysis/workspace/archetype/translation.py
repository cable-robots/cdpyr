from __future__ import annotations

import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.kinematics.transformation import Angular
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Translation(_archetype.Archetype):
    """
    The `translation` workspace is given through the poses with
        the positions in R3
    for which
        the rotation is fixed to R0
    and the observed criterion is valid
    """

    angular: Angular
    dcm: Matrix

    def __init__(self, dcm: Matrix = None, angular: Angular = None, **kwargs):
        super().__init__(**kwargs)

        if dcm is not None and angular is None:
            angular = Angular(dcm)
        elif dcm is None and angular is None:
            angular = Angular(_np.eye(3))

        self.dcm = angular.dcm
        self.angular = angular

    @property
    def comparator(self):
        return all

    def _poses(self, coordinate: Vector):
        return [_pose.Pose(coordinate, self.dcm)]


__all__ = [
        'Translation',
]
