from __future__ import annotations

from abc import ABC, abstractmethod

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'


class Object(ABC):

    def __init__(self, *args, **kwargs):
        pass


class Algorithm(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Algorithm:
        raise NotImplementedError()


class Result(Object):

    def __init__(self, algorithm: Algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._algorithm = algorithm

    @property
    def algorithm(self):
        return self._algorithm


__all__ = [
        'Algorithm',
        'Object',
        'Result',
]
