from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Translation',
]

import numpy as _np

from cdpyr.analysis.archetype import archetype as _archetype
from cdpyr.kinematics.transformation import Angular
from cdpyr.motion import pose as _pose
from cdpyr.typing import Matrix, Vector


class Translation(_archetype.Archetype):
    """
    The `translation` workspace is given through the poses with
        the positions in R3
    for which
        the rotation is fixed to R0
    and the observed criterion is valid
    """

    _angular: Angular
    _dcm: Matrix

    def __init__(self, dcm: Matrix = None, angular: Angular = None, **kwargs):
        super().__init__(**kwargs)

        if dcm is not None and angular is None:
            angular = Angular(dcm)
        elif dcm is None and angular is None:
            angular = Angular(_np.eye(3))

        self._dcm = angular.dcm
        self._angular = angular

    @property
    def angular(self):
        return self.angular

    @property
    def comparator(self):
        return all

    @property
    def dcm(self):
        return self.dcm

    def _poses(self, coordinate: Vector):
        return [_pose.Pose(coordinate, self._dcm)]
