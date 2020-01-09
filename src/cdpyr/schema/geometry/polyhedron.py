from marshmallow import fields

from cdpyr.geometry import polyhedron as _polyhedron
from cdpyr.schema.geometry import primitive as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PolyhedronSchema(_geometry.PrimitiveSchema):
    vertices = fields.List(
            fields.Tuple((fields.Float(required=True),
                          fields.Float(required=True),
                          fields.Float(required=True))
                         ),
            required=True,
    )

    faces = fields.List(
            fields.Tuple((fields.Integer(required=True),
                          fields.Integer(required=True),
                          fields.Integer(required=True))
                         ),
            required=True,
    )

    __model__ = _polyhedron.Polyhedron


__all__ = [
        'PolyhedronSchema',
]
