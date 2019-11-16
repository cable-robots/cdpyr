from marshmallow import fields

from cdpyr.geometry import cuboid as _cuboid
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CuboidSchema(_geometry.GeometrySchema):
    width = fields.Float(
        required=True
    )
    depth = fields.Float(
        required=True
    )
    height = fields.Float(
        required=True
    )

    __model__ = _cuboid.Cuboid


__all__ = [
    'CuboidSchema',
]
