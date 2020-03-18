from __future__ import annotations

import numpy as _np

from cdpyr.analysis.archetype import archetype as _archetype

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Maximum(_archetype.ArchetypeOrientation):
    """
    The `Maximum` workspace is given through the poses with
        the positions in R3
    for which
        one rotation in SO3
    and the observed criterion is valid.
    In math terms this reads
    """

    def __init__(self, steps: int = 10, **kwargs):
        euler = _np.pi * _np.asarray([1.0, 1.0, 1.0])
        super().__init__(euler_min=-euler,
                         euler_max=+euler,
                         sequence='xyz',
                         steps=steps,
                         **kwargs)

    @property
    def comparator(self):
        return any


__all__ = [
        'Maximum',
]
