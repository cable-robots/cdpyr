from marshmallow import Schema, fields, post_load

from cdpyr.robot import robot as _robot
from cdpyr.schema.robot import (
    cable as _cable,
    frame as _frame,
    kinematic_chain as _kinematicchain,
    platform as _platform,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class RobotSchema(Schema):
    name = fields.Str()
    frame = fields.Nested(
        _frame.FrameSchema,
        required=True
    )
    platforms = fields.List(
        fields.Nested(_platform.PlatformSchema),
        required=True
    )
    cables = fields.List(
        fields.Nested(_cable.CableSchema),
        required=True
    )
    kinematic_chains = fields.List(
        fields.Nested(_kinematicchain.KinematicChainSchema),
        required=True
    )

    __model__ = _robot.Robot

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'RobotSchema',
]
