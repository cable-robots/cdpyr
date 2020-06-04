from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'PoseSchema',
]

from marshmallow import fields, post_load

from cdpyr.motion import pose as _pose
from cdpyr.schema import fields as custom_fields
from cdpyr.schema.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)
from cdpyr.schema.schema import Schema


class PoseSchema(Schema):
    time = custom_fields.numpy.Numpy(
            missing=None
    )
    linear = fields.Nested(
            _linear.LinearSchema,
            missing=None
    )
    angular = fields.Nested(
            _angular.AngularSchema,
            missing=None
    )

    __model__ = _pose.Pose

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _pose.PoseList((self.make_object(each, False)
                                   for each in data))
        else:
            return self.__model__(**data)
