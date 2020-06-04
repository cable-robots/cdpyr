from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'TubeSchema',
]

from marshmallow import fields

from cdpyr.geometry import tube as _tube
from cdpyr.schema.geometry import primitive as _geometry


class TubeSchema(_geometry.PrimitiveSchema):
    inner_radius = fields.Tuple(
            (fields.Float(), fields.Float()),
    )
    outer_radius = fields.Tuple(
            (fields.Float(), fields.Float()),
    )
    height = fields.Float(
            required=True
    )

    __model__ = _tube.Tube
