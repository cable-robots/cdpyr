from __future__ import annotations

import numpy as _np

from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Dextrous(_archetype_orientation.ArchetypeOrientation):
    """
    The `Dextrous` workspace is given through the poses with
        the positions in R3
    for which
        all rotations in SO3
    and the observed criterion is valid
    """

    def __init__(self, steps: int = 10, **kwargs):
        euler = _np.pi * _np.asarray([1.0, 1.0, 1.0])
        super().__init__(-euler, +euler, 'xyz', steps, **kwargs)

    @property
    def comparator(self):
        return all


__all__ = [
        'Dextrous',
]
