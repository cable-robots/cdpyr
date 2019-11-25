import numpy as _np

from cdpyr import validator as _validator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import generator as _generator, pose as _pose
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

    _dcm: Matrix

    def __init__(self, dcm: Matrix = None):
        self.dcm = dcm if dcm is not None else _np.eye(3)

    @property
    def comparator(self):
        return all

    @property
    def dcm(self):
        return self._dcm

    @dcm.setter
    def dcm(self, dcm: Matrix):
        _validator.linalg.rotation_matrix(dcm, 'dcm')

        self._dcm = dcm

    @dcm.deleter
    def dcm(self):
        del self._dcm

    def _poses(self, coordinate: Vector):
        return _generator.steps(
            _pose.Pose(coordinate, self._dcm),
            _pose.Pose(coordinate, self._dcm),
            1
        )


__all__ = [
    'Translation',
]
