import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Dextrous(_archetype_orientation.ArchetypeOrientation):

    def __init__(self, step: int = 10):
        euler = _np.pi * _np.asarray([1.0, 1.0, 1.0])
        super().__init__(-euler, +euler, 'xyz', step)

    @property
    def comparator(self):
        return all


__all__ = [
    'Dextrous',
]
