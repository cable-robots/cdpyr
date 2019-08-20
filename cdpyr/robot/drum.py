from typing import Optional, Sequence, Tuple, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.geometry.geometry import Geometry, GeometrySchema
from cdpyr.mechanics.inertia import Inertia, InertiaSchema

from cdpyr.typedefs import Num, Vector, Matrix


class Drum(object):
    _geometry: Geometry
    _inertia: Inertia

    def __init__(self,
                 geometry: Optional[Geometry] = None,
                 inertia: Optional[Union[Tuple[Union[Num, Vector], Union[
                     Vector, Matrix]], Inertia]] = None
                 ):
        self.geometry = geometry or Geometry()
        self.inertia = inertia or Inertia()

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, geometry: Geometry):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self.geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self,
                froinertia: Union[Tuple[Union[Num, Vector], Union[
                    Vector, Matrix]], Inertia]):
        if not isinstance(inertia, Inertia):
            inertia = Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self.inertia


Drum.__repr__ = make_repr(
    'geometry',
    'inertia'
)


class DrumSchema(Schema):
    geometry = fields.Nested(GeometrySchema)
    inertia = fields.Nested(InertiaSchema)

    __model__ = Drum

    @post_load
    def make_user(self, data):
        return self.__model__(**data)


__all__ = ['Drum']
