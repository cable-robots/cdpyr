from marshmallow import Schema, fields, post_load

from cdpyr.geometry import Cuboid, Cylinder, EllipticCylinder, Sphere, Tube
from cdpyr.robot import drum as _drum
from cdpyr.schema import fields as custom_fields
from cdpyr.schema.geometry import (
    CuboidSchema,
    CylinderSchema,
    EllipticCylinderSchema,
    SphereSchema,
    TubeSchema,
)
from cdpyr.schema.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DrumSchema(Schema):
    geometry = fields.Nested(
        _geometry.GeometrySchema,
        missing=None
    )
    inertia = fields.Nested(
        _inertia.InertiaSchema,
        missing=None
    )

    __model__ = _drum.Drum

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'DrumSchema',
]
