from marshmallow import Schema, fields, post_load

from cdpyr.motion.pose import pose as _pose


class PoseSchema(Schema):
    time = fields.Float()
    position = fields.List(fields.List(fields.Float()))
    velocity = fields.List(fields.List(fields.Float()))
    acceleration = fields.List(fields.List(fields.Float()))

    __model__ = _pose.Pose

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class PoseListSchema(Schema):
    data = fields.List(fields.Nested(PoseSchema))

    __model__ = _pose.PoseList

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'PoseSchema',
    'PoseListSchema',
]
