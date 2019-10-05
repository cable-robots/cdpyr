from marshmallow import Schema, fields, post_load

from cdpyr.kinematics.transformation import angular as _angular


class AngularSchema(Schema):
    dcm = fields.List(fields.List(fields.Float()))
    angular_velocity = fields.List(fields.Float())
    angular_acceleration = fields.List(fields.Float())

    __model__ = _angular.Angular

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'AngularSchema',
]
