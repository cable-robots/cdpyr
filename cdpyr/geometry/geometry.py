from abc import ABC

from magic_repr import make_repr


class Geometry(ABC):

    def moment_of_inertia(self, mass: float):
        raise NotImplementedError('method not implemented by child class.')


Geometry.__repr__ = make_repr()

__all__ = ['Geometry']
