from abc import ABC

from magic_repr import make_repr

from cdpyr.typedef import Num


class Geometry(ABC):
    _mass: float

    def moment_of_inertia(self):
        raise NotImplementedError('method not implemented by child class.')

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: Num):
        if mass < 0:
            raise ValueError('mass must be nonnegative')

        self._mass = mass

    @mass.deleter
    def mass(self):
        del self._mass


Geometry.__repr__ = make_repr()

__all__ = [
    'Geometry',
]
