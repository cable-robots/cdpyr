from marshmallow import fields

from cdpyr.geometry import cylinder as _cylinder
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CylinderSchema(_geometry.GeometrySchema):
    diameter = fields.Float(
            required=True
    )
    height = fields.Float(
            required=True
    )

    __model__ = _cylinder.Cylinder


__all__ = [
        'CylinderSchema',
]
