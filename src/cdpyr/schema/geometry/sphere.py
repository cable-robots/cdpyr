from marshmallow import fields

from cdpyr.geometry import sphere as _sphere
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class SphereSchema(_geometry.GeometrySchema):
    diameter = fields.Float(
        required=True
    )

    __model__ = _sphere.Sphere


__all__ = [
    'SphereSchema',
]
