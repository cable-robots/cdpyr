from __future__ import annotations

from cdpyr.analysis.archetype import archetype as _archetype

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class InclusionOrientation(_archetype.ArchetypeOrientation):
    """
    The `InclusionOrientation` workspace is given through the poses with the
    positions in R3 for which one rotation in a set of rotations R0 and the
    observed criterion is valid
    """

    @property
    def comparator(self):
        return any


__all__ = [
        'InclusionOrientation',
]
