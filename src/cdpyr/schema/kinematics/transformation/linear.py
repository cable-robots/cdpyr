from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'LinearSchema',
]

from marshmallow import fields, post_load

from cdpyr.kinematics.transformation import linear as _linear
from cdpyr.schema.schema import Schema


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
