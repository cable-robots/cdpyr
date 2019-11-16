from marshmallow import fields

from cdpyr.geometry import tube as _tube
from cdpyr.schema.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class TubeSchema(_geometry.GeometrySchema):
    inner_diameter = fields.Float(
        required=True
    )
    outer_diameter = fields.Float(
        required=True
    )
    height = fields.Float(
        required=True
    )

    __model__ = _tube.Tube


__all__ = [
    'TubeSchema',
]
