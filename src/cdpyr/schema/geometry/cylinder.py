from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'CylinderSchema',
]

from marshmallow import fields

from cdpyr.geometry import cylinder as _cylinder
from cdpyr.schema.geometry import primitive as _geometry


class CylinderSchema(_geometry.PrimitiveSchema):
    height = fields.Float(
            required=True
    )
    radius = fields.Tuple(
            (fields.Float(), fields.Float()),
            required=True
    )

    __model__ = _cylinder.Cylinder
