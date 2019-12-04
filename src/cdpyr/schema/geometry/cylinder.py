from marshmallow import fields

from cdpyr.geometry import cylinder as _cylinder
from cdpyr.schema.geometry import primitive as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CylinderSchema(_geometry.PrimitiveSchema):
    height = fields.Float(
            required=True
    )
    radius = fields.Tuple(
            (fields.Float(), fields.Float()),
            required=True
    )

    __model__ = _cylinder.Cylinder


__all__ = [
        'CylinderSchema',
]
