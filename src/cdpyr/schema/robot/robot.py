from marshmallow import Schema, fields, post_load

from cdpyr.robot import (
    cable as _cable,
    frame as _frame,
    kinematicchain as _kinematicchain,
    platform as _platform,
    robot as _robot,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class RobotSchema(Schema):
    name = fields.AnyStr()
    frame = fields.Nested(_frame.FrameSchema)
    platforms = fields.List(fields.Nested(_platform.PlatformSchema))
    cables = fields.List(fields.Nested(_cable.CableSchema))
    kinematic_chains = fields.List(
        fields.Nested(_kinematicchain.KinematicChainSchema))

    __model__ = _robot.Robot

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'RobotSchema',
]
