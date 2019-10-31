from marshmallow import Schema, fields, post_load

from cdpyr.motion.pattern import motion_pattern as _motion_pattern

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPatternSchema(Schema):
    translation = fields.Int()
    rotation = fields.Int()

    __model__ = _motion_pattern.MotionPattern

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'MotionPatternSchema',
]
