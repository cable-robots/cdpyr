from typing import AnyStr, Sequence

from abc import ABC, abstractmethod

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Parser(ABC):

    @abstractmethod
    def encode(self, obj: object, *args, **kwargs) -> AnyStr:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, stream: AnyStr, *args, **kwargs) -> object:
        raise NotImplementedError()
