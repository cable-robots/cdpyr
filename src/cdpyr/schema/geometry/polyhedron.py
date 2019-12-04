from marshmallow import fields

from cdpyr.geometry import polyhedron as _polyhedron
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PolyhedronSchema(_geometry.GeometrySchema):
    vertices = fields.List(
            fields.Tuple(
                    (fields.Float(required=True),
                     fields.Float(required=True),
                     fields.Float(required=True))
            ),
            required=True,
    )
    faces = fields.List(
            fields.Tuple(
                    (fields.Float(required=True),
                     fields.Float(required=True),
                     fields.Float(required=True))
            ),
            required=True,
    )

    __model__ = _polyhedron.Polyhedron


__all__ = [
        'PolyhedronSchema',
]
