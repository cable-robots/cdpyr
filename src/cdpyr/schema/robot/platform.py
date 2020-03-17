from marshmallow import fields, post_load

from cdpyr.robot import platform as _platform
from cdpyr.schema.schema import Schema
from cdpyr.schema.mechanics import inertia as _inertia
from cdpyr.schema.motion import pose as _pose
from cdpyr.schema.motion.pattern import pattern as _pattern
from cdpyr.schema.robot.anchor import platform_anchor as _platform_anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformSchema(Schema):
    name = fields.String(
            required=False,
            missing='default',
    )
    anchors = fields.Nested(
            _platform_anchor.PlatformAnchorSchema(
                    many=True,
            ),
            required=True,
    )
    pose = fields.Nested(
            _pose.PoseSchema,
            missing=None
    )
    motion_pattern = fields.Nested(
            _pattern.PatternSchema,
            required=True,
    )
    center_of_gravity = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=False,
            missing=(0.0, 0.0, 0.0),
    )
    center_of_linkage = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=False,
            missing=(0.0, 0.0, 0.0),
    )
    inertia = fields.Nested(
            _inertia.InertiaSchema,
            required=False,
            missing=None,
    )

    __model__ = _platform.Platform

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _platform.PlatformList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'PlatformSchema',
]
