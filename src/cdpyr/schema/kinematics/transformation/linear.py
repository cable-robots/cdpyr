from marshmallow import Schema, fields, post_load

from cdpyr.kinematics.transformation import linear as _linear

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class LinearSchema(Schema):
    position = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            missing=None
    )
    velocity = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            missing=None
    )
    acceleration = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            missing=None
    )

    __model__ = _linear.Linear

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'LinearSchema',
]
