from marshmallow import fields

from cdpyr.robot.anchor import frame_anchor as _frame_anchor
from cdpyr.schema.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.schema.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameAnchorSchema(_anchor.AnchorSchema):
    pulley = fields.Nested(_pulley.PulleySchema)
    drivetrain = fields.Nested(_drivetrain.DriveTrainSchema)

    __model__ = _frame_anchor.FrameAnchor


class FrameAnchorListSchema(_anchor.AnchorListSchema):
    data = fields.Nested(FrameAnchorSchema)

    __model__ = _frame_anchor.FrameAnchorList


__all__ = [
    'FrameAnchorSchema',
    'FrameAnchorListSchema',
]
