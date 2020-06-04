from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'EllipsoidSchema',
]

from marshmallow import fields

from cdpyr.geometry import ellipsoid as _ellipsoid
from cdpyr.schema.geometry import primitive as _geometry


class EllipsoidSchema(_geometry.PrimitiveSchema):
    radius = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=True
    )

    __model__ = _ellipsoid.Ellipsoid
