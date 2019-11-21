from abc import ABC

from cdpyr.mixin.base_object import BaseObject

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Geometry(ABC, BaseObject):
    pass


__all__ = [
    'Geometry',
]
