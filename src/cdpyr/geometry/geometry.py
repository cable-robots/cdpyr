from abc import ABC, abstractmethod

from cdpyr.mixin.base_object import BaseObject

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Geometry(ABC, BaseObject):

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        raise NotImplementedError()


__all__ = [
        'Geometry',
]
