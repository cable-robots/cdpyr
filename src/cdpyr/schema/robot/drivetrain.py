from marshmallow import fields

from cdpyr.schema.schema import Schema
from cdpyr.schema.robot import (
    drum as _drum,
    gearbox as _gearbox,
    motor as _motor
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DriveTrainSchema(Schema):
    motor = fields.Nested(
            _motor.MotorSchema,
            missing=None
    )
    gearbox = fields.Nested(
            _gearbox.GearboxSchema,
            missing=None
    )
    drum = fields.Nested(
            _drum.DrumSchema,
            missing=None
    )


__all__ = [
        'DriveTrainSchema'
]
