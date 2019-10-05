from marshmallow import fields

from cdpyr.robot.anchor import platformanchor as _platformanchor
from cdpyr.schema.robot.anchor import anchor as _anchor


class PlatformAnchorSchema(_anchor.AnchorSchema):
    __model__ = _platformanchor.PlatformAnchor


class PlatformAnchorListSchema(_anchor.AnchorListSchema):
    data = fields.Nested(PlatformAnchorSchema)

    __model__ = _platformanchor.PlatformAnchorList


__all__ = [
    'PlatformAnchorSchema',
    'PlatformAnchorListSchema',
]
