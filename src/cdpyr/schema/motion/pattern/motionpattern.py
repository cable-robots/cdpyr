from marshmallow import Schema, fields, post_load

from cdpyr.motion import pattern as _pattern


class MotionpatternSchema(Schema):
    translation = fields.Int()
    rotation = fields.Int()

    __model__ = _pattern.Motionpattern

    @post_load
    def make_object(self, data, **kwargs):
        #     # algorithm_map = {
        #     #     '1T': Motionpattern._1T,
        #     #     '2T': Motionpattern._2T,
        #     #     '3T': Motionpattern._3T,
        #     #     '1R2T': Motionpattern._1R2T,
        #     #     '2R3T': Motionpattern._2R3T,
        #     #     '3R3T': Motionpattern._3R3T,
        #     # }
        #
        #     # human = data
        return self.__model__(**data)


__all__ = [
    'MotionpatternSchema',
]
