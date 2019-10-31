from cdpyr.analysis.workspace.archetype import archetype_orientation as \
    _archetype_orientation

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class InclusionOrientation(_archetype_orientation.ArchetypeOrientation):

    @property
    def comparator(self):
        return any


__all__ = [
    'InclusionOrientation',
]
