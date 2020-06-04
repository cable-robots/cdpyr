from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'FrameSchema',
        'FrameAnchorSchema',
]

from marshmallow import fields, post_load

import cdpyr.robot
from cdpyr.robot import frame as _frame
from cdpyr.schema.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.schema.robot.anchor import AnchorSchema
from cdpyr.schema.schema import Schema


class FrameAnchorSchema(AnchorSchema):
    pulley = fields.Nested(
            _pulley.PulleySchema,
            missing=None
    )
    drivetrain = fields.Nested(
            _drivetrain.DriveTrainSchema,
            missing=None
    )

    __model__ = cdpyr.robot.frame.FrameAnchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return cdpyr.robot.frame.FrameAnchorList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


class FrameSchema(Schema):
    anchors = fields.Nested(
            FrameAnchorSchema(
                    many=True
            ),
            required=True,
    )

    __model__ = _frame.Frame

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
