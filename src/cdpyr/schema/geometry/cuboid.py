from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'CuboidSchema',
]

from marshmallow import fields

from cdpyr.geometry import cuboid as _cuboid
from cdpyr.schema.geometry import primitive as _geometry


class CuboidSchema(_geometry.PrimitiveSchema):
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
