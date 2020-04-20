from __future__ import annotations

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__all__ = [
        'Algorithm',
        'Object',
        'Result',
]

from abc import ABC, abstractmethod


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
