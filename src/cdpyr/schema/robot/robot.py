from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'RobotSchema',
]

from marshmallow import fields, post_load

from cdpyr.robot import robot as _robot
from cdpyr.schema.motion.pose import pose as _pose
from cdpyr.schema.robot import (
    cable as _cable,
    frame as _frame,
    kinematic_chain as _kinematicchain,
    platform as _platform,
)
from cdpyr.schema.schema import Schema


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
    home_pose = fields.Nested(
            _pose.PoseSchema,
    )

    __model__ = _robot.Robot

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
