from marshmallow import Schema, fields, post_load

from cdpyr.motion import pattern as _pattern


class MotionpatternSchema(Schema):
    translation = fields.Int()
    rotation = fields.Int()

    __model__ = _pattern.Motionpattern

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'MotionpatternSchema',
]
