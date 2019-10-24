from marshmallow import Schema, fields, post_load

from cdpyr.kinematics.transformation import linear as _linear

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class LinearSchema(Schema):
    position = fields.List(fields.Float())
    velocity = fields.List(fields.Float())
    acceleration = fields.List(fields.Float())

    __model__ = _linear.Linear

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'LinearSchema',
]
