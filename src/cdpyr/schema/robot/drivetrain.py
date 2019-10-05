from marshmallow import Schema, fields

from cdpyr.schema.robot import (
    drum as _drum,
    gearbox as _gearbox,
    motor as _motor,
)


class DriveTrainSchema(Schema):
    motor = fields.Nested(_motor.MotorSchema)
    gearbox = fields.Nested(_gearbox.GearboxSchema)
    drum = fields.Nested(_drum.DrumSchema)


__all__ = [
    'DriveTrainSchema'
]
