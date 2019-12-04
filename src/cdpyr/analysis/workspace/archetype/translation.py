import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import pose as _pose
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

    dcm: Matrix

    def __init__(self, dcm: Matrix = None, **kwargs):
        super().__init__(**kwargs)
        self.dcm = dcm if dcm is not None else _np.eye(3)

    @property
    def comparator(self):
        return all

    def _poses(self, coordinate: Vector):
        return [_pose.Pose(coordinate, self.dcm)]


__all__ = [
        'Translation',
]
