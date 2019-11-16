from marshmallow import Schema, fields, post_load

from cdpyr.robot import kinematicchain as _kinematicchain
from cdpyr.schema.robot import cable as _cable, platform as _platform
from cdpyr.schema.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicChainSchema(Schema):
    frame_anchor = fields.Nested(
        _frame_anchor.FrameAnchorSchema,
        required=True
    )
    platform = fields.Nested(
        _platform.PlatformSchema,
        required=True
    )
    platform_anchor = fields.Nested(
        _platform_anchor.PlatformAnchorSchema,
        required=True
    )
    cable = fields.Nested(
        _cable.CableSchema,
        required=True
    )

    __model__ = _kinematicchain.KinematicChain

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _kinematicchain.KinematicChainList(
                (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
    'KinematicChainSchema',
]
