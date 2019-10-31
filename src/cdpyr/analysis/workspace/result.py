import copy
from abc import ABC

from cdpyr.analysis.workspace import algorithm as _workspace
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):
    _algorithm: '_workspace.Algorithm'
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'

    def __init__(self,
                 algorithm: '_workspace.Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self._algorithm = copy.deepcopy(algorithm)
        self._archetype = copy.deepcopy(archetype)
        self._criterion = copy.deepcopy(criterion)

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion


__all__ = [
    'Result',
]
