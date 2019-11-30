from marshmallow import fields

from cdpyr.geometry import elliptic_cylinder as _elliptic_cylinder
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class EllipticCylinderSchema(_geometry.GeometrySchema):
    major_diameter = fields.Float(
            required=True
    )
    minor_diameter = fields.Float(
            required=True
    )
    height = fields.Float(
            required=True
    )

    __model__ = _elliptic_cylinder.EllipticCylinder


__all__ = [
    'EllipticCylinderSchema',
]
