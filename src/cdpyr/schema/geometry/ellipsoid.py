from marshmallow import fields

from cdpyr.geometry import ellipsoid as _ellipsoid
from cdpyr.schema.geometry import primitive as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class EllipsoidSchema(_geometry.PrimitiveSchema):
    radius = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=True
    )

    __model__ = _ellipsoid.Ellipsoid


__all__ = [
        'EllipsoidSchema',
]
