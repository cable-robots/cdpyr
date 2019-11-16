from cdpyr.schema.robot.anchor import (
    # AnchorListSchema,
    AnchorSchema,
    # FrameAnchorListSchema,
    FrameAnchorSchema,
    # PlatformAnchorListSchema,
    PlatformAnchorSchema,
)
from cdpyr.schema.robot.cable import CableSchema
# from cdpyr.schema.robot.cable import CableListSchema, CableSchema
from cdpyr.schema.robot.drivetrain import DriveTrainSchema
from cdpyr.schema.robot.drum import DrumSchema
from cdpyr.schema.robot.frame import FrameSchema
from cdpyr.schema.robot.gearbox import GearboxSchema
from cdpyr.schema.robot.kinematic_chain import (
    # KinematicChainListSchema,
    KinematicChainSchema,
)
from cdpyr.schema.robot.motor import MotorSchema
from cdpyr.schema.robot.platform import PlatformSchema
# from cdpyr.schema.robot.platform import PlatformListSchema, PlatformSchema
from cdpyr.schema.robot.pulley import PulleySchema
from cdpyr.schema.robot.robot import RobotSchema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

__all__ = [
    'AnchorSchema',
    # 'AnchorListSchema',
    'FrameAnchorSchema',
    # 'FrameAnchorListSchema',
    'PlatformAnchorSchema',
    # 'PlatformAnchorListSchema',
    'CableSchema',
    # 'CableListSchema',
    'DrumSchema',
    'DriveTrainSchema',
    'FrameSchema',
    'GearboxSchema',
    'KinematicChainSchema',
    # 'KinematicChainListSchema',
    'MotorSchema',
    'PlatformSchema',
    # 'PlatformListSchema',
    'PulleySchema',
    'RobotSchema',
]
