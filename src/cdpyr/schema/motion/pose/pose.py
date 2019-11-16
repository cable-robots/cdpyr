import numpy as _np
from marshmallow import Schema, fields, post_load

from cdpyr.motion.pose import pose as _pose, poselist as _pose_list
from cdpyr.schema.kinematics.transformation import (
    angular as _angular,
    linear as _linear,
)
from cdpyr.stream.marshmallow import fields as custom_fields

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


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
            return _pose_list.PoseList(
                (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
    'PoseSchema',
]
