from abc import abstractmethod
from typing import Union

from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Matrix, Vector


class Transformation(BaseObject):

    @abstractmethod
    def apply(self, coordinates: Union[Vector, Matrix]):
        raise NotImplementedError()


__all__ = [
        'Transformation',
]
