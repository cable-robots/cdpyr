from marshmallow import fields

from cdpyr.schema.cdpyr_schema import CdpyrSchema
from cdpyr.schema.robot import (
    drum as _drum,
    gearbox as _gearbox,
    motor as _motor
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DriveTrainSchema(CdpyrSchema):
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
