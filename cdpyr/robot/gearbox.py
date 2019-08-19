from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Gearbox(object):
    _ratio: _TVector
    _moment_of_inertia: _TNum

    def __init__(self,
                 ratio: Optional[_TNum] = None,
                 inertia: Optional[_TNum] = None
                 ):
        self.ratio = ratio or None
        self.inertia = inertia or None

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, ratio: _TNum):
        if ratio < 0:
            raise ValueError('ratio must be nonnegative.')

        self._ratio = ratio

    @ratio.deleter
    def ratio(self):
        del self._ratio

    @property
    def moment_of_inertia(self):
        return self._moment_of_inertia

    @moment_of_inertia.setter
    def moment_of_inertia(self, inertia: _TNum):
        if inertia < 0:
            raise ValueError('moment_of_inertia must be nonnegative.')

        self._moment_of_inertia = inertia

    @moment_of_inertia.deleter
    def moment_of_inertia(self):
        del self._moment_of_inertia


Gearbox.__repr__ = make_repr(
    'ratio',
    'moment_of_inertia'
)


class GearboxSchema(Schema):
    ratio = fields.Float()
    moment_of_inertia = fields.Float()

    __model__ = Gearbox

    @post_load
    def make_gearbox(self, data):
        return self.__model__(**data)


__all__ = ['Gearbox', 'GearboxSchema']
