from marshmallow import Schema, fields, post_load

from cdpyr.robot.anchor import anchor as _anchor
from cdpyr.schema.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class AnchorSchema(Schema):
    position = fields.Nested(_linear.LinearSchema)
    dcm = fields.Nested(_angular.AngularSchema)

    __model__ = _anchor.Anchor

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class AnchorListSchema(Schema):
    data = fields.Nested(AnchorSchema)

    __model__ = _anchor.AnchorList

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'AnchorSchema',
    'AnchorListSchema',
]
