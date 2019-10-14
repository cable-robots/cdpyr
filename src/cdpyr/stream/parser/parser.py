from typing import AnyStr, Sequence

from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def encode(self, obj: object, *args, **kwargs) -> Sequence[AnyStr]:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, stream: AnyStr, *args, **kwargs) -> object:
        raise NotImplementedError()
