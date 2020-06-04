from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'TotalOrientation',
]

from cdpyr.analysis.archetype import archetype as _archetype


class TotalOrientation(_archetype.ArchetypeOrientation):
    """
    The `TotalOrientation` workspace is given through the poses with the
    positions in R3 for which all rotations in a set of rotations R0 and the
    observed criterion is valid
    """

    @property
    def comparator(self):
        return all
