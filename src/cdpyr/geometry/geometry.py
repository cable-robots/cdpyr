from abc import ABC, abstractmethod
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Geometry(ABC):
    _mass: float

    @abstractmethod
    def moment_of_inertia(self):
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
