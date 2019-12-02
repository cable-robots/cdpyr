from abc import ABC, abstractmethod

from cdpyr.mixin.base_object import BaseObject

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Geometry(ABC, BaseObject):

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError()

    def __hash__(self, other):
        raise NotImplementedError()


__all__ = [
        'Geometry',
]
