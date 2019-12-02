from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class TotalOrientation(_archetype_orientation.ArchetypeOrientation):
    """
    The `TotalOrientation` workspace is given through the poses with
        the positions in R3
    for which
        all rotations in a set of rotations R0
    and the observed criterion is valid
    """

    @property
    def comparator(self):
        return all


__all__ = [
        'TotalOrientation',
]
