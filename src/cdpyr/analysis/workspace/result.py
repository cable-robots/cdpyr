import copy
from abc import ABC, abstractmethod

from cdpyr.analysis.workspace import algorithm as _workspace
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(ABC):
    _algorithm: '_workspace.Algorithm'
    _archetype: '_archetype.Archetype'
    _criterion: '_criterion.Criterion'
    _surface: float
    _volume: float

    def __init__(self,
                 algorithm: '_workspace.Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        self._algorithm = copy.deepcopy(algorithm)
        self._archetype = copy.deepcopy(archetype)
        self._criterion = copy.deepcopy(criterion)
        self._surface = None
        self._volume = None

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def archetype(self):
        return self._archetype

    @property
    def criterion(self):
        return self._criterion

    @property
    @abstractmethod
    def surface(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def volume(self):
        raise NotImplementedError()


__all__ = [
    'Result',
]
