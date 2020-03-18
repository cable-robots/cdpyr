# TODO We should have a `something` that represents a wrench object to which
#  you'd pass the robot, the pose, and the gravitational constant (or maybe
#  the vector of gravitational forces) that then converts this into a (
#  sequence of) vectors representing the wrench vector acting on the
#  platforms center of gravity. Or we'll add this to the `robot.Robot` object
#  as a method...

from cdpyr.robot.cable import Cable, CableList
from cdpyr.robot.drivetrain import Drivetrain
from cdpyr.robot.drum import Drum
from cdpyr.robot.frame import Frame, FrameAnchor, FrameAnchorList
from cdpyr.robot.gearbox import Gearbox
from cdpyr.robot.kinematicchain import KinematicChain, KinematicChainList
from cdpyr.robot.motor import Motor
from cdpyr.robot.platform import (
    Platform,
    PlatformAnchor,
    PlatformAnchorList,
    PlatformList
)
from cdpyr.robot.pulley import Pulley
from cdpyr.robot.robot import Robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

__all__ = [
        'Cable',
        'CableList',
        'Drum',
        'Drivetrain',
        'Frame',
        'FrameAnchor',
        'FrameAnchorList',
        'Gearbox',
        'KinematicChain',
        'KinematicChainList',
        'Motor',
        'Platform',
        'PlatformAnchor',
        'PlatformAnchorList',
        'PlatformList',
        'Pulley',
        'Robot',
]
