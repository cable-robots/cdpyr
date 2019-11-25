import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation
from cdpyr.motion.pose import generator as _generator, pose as _pose
from cdpyr.typing import Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Orientation(_archetype_orientation.ArchetypeOrientation):
    """
    The `Orientation` workspace is given through the poses with
        the rotations in SO3
    for which
        the position is fixed in R3
    and the observed criterion is valid
    """

    def __init__(self, position: Vector, step: int = 10):
        self.position = position
        euler = _np.pi * _np.asarray([+1.0, +1.0, +1.0])
        super().__init__(-euler, +euler, 'xyz', step)

    @property
    def comparator(self):
        return all

    def _poses(self, *args, **kwargs):
        return _generator.steps(
            _pose.Pose(
                self.position,
                _generator.from_euler(self.sequence, self.euler_min)
            ),
            _pose.Pose(
                self.position,
                _generator.from_euler(self.sequence, self.euler_max)
            ),
            self.step
        )


__all__ = [
    'Orientation',
]
