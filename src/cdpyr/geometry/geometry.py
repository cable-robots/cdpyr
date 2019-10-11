from abc import ABC, abstractmethod
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.typing import Num


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
        _validator.positive(mass, 'mass')

        self._mass = mass

    @mass.deleter
    def mass(self):
        del self._mass


Geometry.__repr__ = make_repr()

__all__ = [
    'Geometry',
]
