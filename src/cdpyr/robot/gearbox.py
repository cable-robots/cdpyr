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
    def moment_of_inertia(self):
        return self._moment_of_inertia

    @moment_of_inertia.setter
    def moment_of_inertia(self, inertia: Num):
        _validator.numeric.positive(inertia, 'inertia')

        self._moment_of_inertia = inertia

    @moment_of_inertia.deleter
    def moment_of_inertia(self):
        del self._moment_of_inertia


Gearbox.__repr__ = make_repr(
    'ratio',
    'moment_of_inertia'
)

__all__ = [
    'Gearbox',
]
