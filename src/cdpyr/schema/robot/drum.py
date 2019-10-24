from marshmallow import Schema, fields, post_load

from cdpyr.robot import drum as _drum
from cdpyr.schema.geometry import geometry as _geometry
from cdpyr.schema.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DrumSchema(Schema):
    geometry = fields.Nested(_geometry.GeometrySchema)
    inertia = fields.Nested(_inertia.InertiaSchema)

    __model__ = _drum.Drum

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'DrumSchema',
]
