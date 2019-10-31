from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class TotalOrientation(_archetype_orientation.ArchetypeOrientation):

    @property
    def comparator(self):
        return all


__all__ = [
    'TotalOrientation',
]
