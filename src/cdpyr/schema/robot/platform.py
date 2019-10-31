from marshmallow import Schema, fields, post_load

from cdpyr.robot import platform as _platform
from cdpyr.schema.motion import pose as _pose
from cdpyr.schema.motion.pattern import motion_pattern as _motion_pattern
from cdpyr.schema.robot.anchor import platformanchor as _platformanchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformSchema(Schema):
    anchors = fields.List(fields.Nested(_platformanchor.PlatformAnchorSchema))
    pose = fields.Nested(_pose.PoseSchema)
    motionpattern = fields.Nested(_motion_pattern.MotionPatternSchema)

    __model__ = _platform.Platform

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class PlatformListSchema(Schema):
    data = fields.List(fields.Nested(PlatformSchema))

    __model__ = _platform.PlatformList

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'PlatformSchema',
    'PlatformListSchema',
]
