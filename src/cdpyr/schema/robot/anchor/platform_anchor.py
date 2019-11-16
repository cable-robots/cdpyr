from marshmallow import fields

from cdpyr.robot.anchor import platform_anchor as _platform_anchor
from cdpyr.schema.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformAnchorSchema(_anchor.AnchorSchema):
    __model__ = _platform_anchor.PlatformAnchor


class PlatformAnchorListSchema(_anchor.AnchorListSchema):
    data = fields.Nested(PlatformAnchorSchema)

    __model__ = _platform_anchor.PlatformAnchorList


__all__ = [
    'PlatformAnchorSchema',
    'PlatformAnchorListSchema',
]
