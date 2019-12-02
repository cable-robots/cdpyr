from marshmallow import fields, post_load

from cdpyr.robot.anchor import frame_anchor as _frame_anchor
from cdpyr.schema.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.schema.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameAnchorSchema(_anchor.AnchorSchema):
    pulley = fields.Nested(
            _pulley.PulleySchema,
            missing=None
    )
    drivetrain = fields.Nested(
            _drivetrain.DriveTrainSchema,
            missing=None
    )

    __model__ = _frame_anchor.FrameAnchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _frame_anchor.FrameAnchorList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'FrameAnchorSchema',
]
