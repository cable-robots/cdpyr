import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Maximum(_archetype_orientation.ArchetypeOrientation):
    """
    The `Maximum` workspace is given through the poses with
        the positions in R3
    for which
        one rotation in SO3
    and the observed criterion is valid.
    In math terms this reads
    """

    def __init__(self, steps: int = 10):
        euler = _np.pi * _np.asarray([1.0, 1.0, 1.0])
        super().__init__(-euler, +euler, 'xyz', steps)

    @property
    def comparator(self):
        return any


__all__ = [
    'Maximum',
]
