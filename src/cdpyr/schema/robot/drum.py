from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'DrumSchema',
]

from marshmallow import fields, post_load

from cdpyr.geometry import Cuboid, Cylinder, Ellipsoid, Polyhedron, Tube
from cdpyr.robot import drum as _drum
from cdpyr.schema import fields as custom_fields
from cdpyr.schema.geometry import (
    CuboidSchema,
    CylinderSchema,
    EllipsoidSchema,
    PolyhedronSchema,
    TubeSchema,
)
from cdpyr.schema.mechanics import inertia as _inertia
from cdpyr.schema.schema import Schema


class DrumSchema(Schema):
    geometry = custom_fields.Polymorphic(
            (
                    (Cuboid, CuboidSchema),
                    (Cylinder, CylinderSchema),
                    (Ellipsoid, EllipsoidSchema),
                    (Polyhedron, PolyhedronSchema),
                    (Tube, TubeSchema),
            ),
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
