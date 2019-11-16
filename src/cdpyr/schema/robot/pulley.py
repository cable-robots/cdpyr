from marshmallow import Schema, fields, post_load

from cdpyr.robot import pulley as _pulley
from cdpyr.schema.geometry import geometry as _geometry
from cdpyr.schema.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PulleySchema(Schema):
    geometry = fields.Nested(
        _geometry.GeometrySchema,
        missing=None
    )
    inertia = fields.Nested(
        _inertia.InertiaSchema,
        missing=None
    )
    dcm = fields.Tuple(
        (
            fields.Tuple(
                (fields.Float(), fields.Float(), fields.Float())
            ),
            fields.Tuple(
                (fields.Float(), fields.Float(), fields.Float())
            ),
            fields.Tuple(
                (fields.Float(), fields.Float(), fields.Float())
            )
        ),
        missing=None
    )

    __model__ = _pulley.Pulley

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'PulleySchema',
]
