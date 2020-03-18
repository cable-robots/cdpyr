from marshmallow import fields, post_load

from cdpyr.robot import anchor as _anchor
from cdpyr.schema.robot import (
    drivetrain as _drivetrain,
    pulley as _pulley
)
from cdpyr.schema.schema import Schema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class AnchorSchema(Schema):
    position = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=True,
    )
    dcm = fields.Tuple((
            fields.Tuple(
                    (fields.Float(), fields.Float(), fields.Float())
            ),
            fields.Tuple(
                    (fields.Float(), fields.Float(), fields.Float())
            ),
            fields.Tuple(
                    (fields.Float(), fields.Float(), fields.Float())
            )),
            missing=None
    )

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _anchor.AnchorList(
                    (self.make_object(each, False, **kwargs) for each in data))
        else:
            return self.__model__(**data)


class FrameAnchorSchema(AnchorSchema):
    pulley = fields.Nested(
            _pulley.PulleySchema,
            missing=None
    )
    drivetrain = fields.Nested(
            _drivetrain.DriveTrainSchema,
            missing=None
    )

    __model__ = _anchor.FrameAnchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _anchor.FrameAnchorList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


class PlatformAnchorSchema(AnchorSchema):
    __model__ = _anchor.PlatformAnchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _anchor.PlatformAnchorList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'FrameAnchorSchema',
        'PlatformAnchorSchema',
]
