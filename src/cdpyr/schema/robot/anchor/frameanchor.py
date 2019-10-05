from marshmallow import fields

from cdpyr.robot.anchor import frameanchor as _frameanchor
from cdpyr.schema.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.schema.robot.anchor import anchor as _anchor


class FrameAnchorSchema(_anchor.AnchorSchema):
    pulley = fields.Nested(_pulley.PulleySchema)
    drivetrain = fields.Nested(_drivetrain.DriveTrainSchema)

    __model__ = _frameanchor.FrameAnchor


class FrameAnchorListSchema(_anchor.AnchorListSchema):
    data = fields.Nested(FrameAnchorSchema)

    __model__ = _frameanchor.FrameAnchorList


__all__ = [
    'FrameAnchorSchema',
    'FrameAnchorListSchema',
]
