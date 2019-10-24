from marshmallow import Schema, fields, post_load

from cdpyr.robot import motor as _motor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotorSchema(Schema):
    torques = fields.Dict()
    rated_power = fields.Float()
    rated_speed = fields.Float()
    moment_of_inertia = fields.Float()

    __model__ = _motor.Motor

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'MotorSchema',
]
