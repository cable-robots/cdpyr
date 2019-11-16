from abc import ABC, abstractmethod
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Geometry(ABC, BaseObject):
    _mass: float

    def __init__(self, mass: Num):
        self.mass = mass

    @abstractmethod
    def inertia(self):
        raise NotImplementedError('method not implemented by child class.')

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: Num):
        _validator.numeric.positive(mass, 'mass')

        self._mass = mass

    @mass.deleter
    def mass(self):
        del self._mass

    __repr__ = make_repr(
        'mass',
    )


__all__ = [
    'Geometry',
]
