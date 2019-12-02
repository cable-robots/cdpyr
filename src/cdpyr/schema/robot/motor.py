from marshmallow import Schema, fields, post_load

from cdpyr.robot import motor as _motor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotorSchema(Schema):
    inertia = fields.Float(
            missing=None
    )
    rated_power = fields.Float(
            missing=None
    )
    rated_speed = fields.Float(
            missing=None
    )
    torques = fields.Dict(
            missing=None,
            keys=fields.String(),
            values=fields.Float(),
    )

    __model__ = _motor.Motor

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'MotorSchema',
]
