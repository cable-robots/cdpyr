from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.mixin.base_object import BaseObject
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Gearbox(BaseObject):
    _inertia: Num
    _ratio: Num

    def __init__(self,
                 ratio: Optional[Num] = None,
                 inertia: Optional[Num] = None
                 ):
        self.ratio = ratio or 1
        self.inertia = inertia or np_.Inf

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, ratio: Num):
        _validator.numeric.nonnegative(ratio, 'ratio')

        self._ratio = ratio

    @ratio.deleter
    def ratio(self):
        del self._ratio

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self, inertia: Num):
        _validator.numeric.positive(inertia, 'inertia')

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.inertia == other.inertia and \
               self.ratio == other.ratio

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.inertia, self.ratio))

    __repr__ = make_repr(
        'ratio',
        'inertia'
    )


__all__ = [
    'Gearbox',
]
