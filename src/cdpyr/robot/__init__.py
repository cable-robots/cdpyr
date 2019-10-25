# TODO We should have a `something` that represents a wrench object to which
#  you'd pass the robot, the pose, and the gravitational constant (or maybe
#  the vector of gravitational forces) that then converts this into a (
#  sequence of) vectors representing the wrench vector acting on the
#  platforms center of gravity. Or we'll add this to the `robot.Robot` object
#  as a method...

from typing import Sequence, Union

from cdpyr.robot.anchor import (
    Anchor,
    AnchorList,
    FrameAnchor,
    FrameAnchorList,
    PlatformAnchor,
    PlatformAnchorList,
)
from cdpyr.robot.cable import Cable, CableList
from cdpyr.robot.drivetrain import DriveTrain
from cdpyr.robot.drum import Drum
from cdpyr.robot.frame import Frame
from cdpyr.robot.gearbox import Gearbox
from cdpyr.robot.kinematicchain import (
    KinematicChain,
    KinematicChainList,
)
from cdpyr.robot.motor import Motor
from cdpyr.robot.platform import Platform, PlatformList
from cdpyr.robot.pulley import Pulley
from cdpyr.robot.robot import Robot

RobotComponent = Union[
    Cable,
    Sequence[Cable],
    CableList,
    DriveTrain,
    Drum,
    Frame,
    FrameAnchor,
    Sequence[FrameAnchor],
    FrameAnchorList,
    Gearbox,
    KinematicChain,
    Sequence[KinematicChain],
    KinematicChainList,
    Motor,
    Platform,
    Sequence[Platform],
    PlatformList,
    PlatformAnchor,
    Sequence[PlatformAnchor],
    PlatformAnchorList,
    Pulley,
    Robot,
]

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

__all__ = [
    'Anchor',
    'AnchorList',
    'FrameAnchor',
    'FrameAnchorList',
    'PlatformAnchor',
    'PlatformAnchorList',
    'Cable',
    'CableList',
    'Drum',
    'DriveTrain',
    'Frame',
    'Gearbox',
    'KinematicChain',
    'KinematicChainList',
    'Motor',
    'Platform',
    'PlatformList',
    'Pulley',
    'Robot',
    'RobotComponent',
]
