from marshmallow import fields

from cdpyr.geometry import tube as _tube
from cdpyr.schema.geometry import primitive as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class TubeSchema(_geometry.PrimitiveSchema):
    inner_radiu = fields.Tuple(
            (fields.Float(), fields.Float()),
    )
    outer_radius = fields.Tuple(
            (fields.Float(), fields.Float()),
    )
    height = fields.Float(
            required=True
    )

    __model__ = _tube.Tube


__all__ = [
        'TubeSchema',
]
