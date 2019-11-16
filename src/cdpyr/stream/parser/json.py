import json
from typing import AnyStr

from cdpyr import motion as _motion, robot as _robot, schema as _schema
from cdpyr.helpers import full_classname as fcn
from cdpyr.stream.parser import parser as _parser

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class JSON(_parser.Parser):
    # define the mapping of object type and marshmallow schemes
    _MAPPING = {
        fcn(_robot.Cable):              _schema.robot.CableSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.CableList):          _schema.robot.CableSchema(
            many=True,
            partial=False
        ),
        fcn(_robot.Drum):               _schema.robot.DrumSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.DriveTrain):         _schema.robot.DriveTrainSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.Frame):              _schema.robot.FrameSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.FrameAnchor):        _schema.robot.FrameAnchorSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.FrameAnchorList):    _schema.robot.FrameAnchorSchema(
            many=True,
            partial=False
        ),
        fcn(_robot.Gearbox):            _schema.robot.GearboxSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.KinematicChain):     _schema.robot.KinematicChainSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.KinematicChainList): _schema.robot.KinematicChainSchema(
            many=True,
            partial=False
        ),
        fcn(_robot.Motor):              _schema.robot.MotorSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.Platform):           _schema.robot.PlatformSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.PlatformList):       _schema.robot.PlatformSchema(
            many=True,
            partial=False
        ),
        fcn(_robot.PlatformAnchor):     _schema.robot.PlatformAnchorSchema(
            many=False,
            partial=False
        ),
        fcn(_robot.PlatformAnchorList): _schema.robot.PlatformAnchorSchema(
            many=True,
            partial=False
        ),
        fcn(_robot.Pulley):             _schema.robot.PulleySchema(
            many=False,
            partial=False
        ),
        fcn(_robot.Robot):              _schema.robot.RobotSchema(
            many=False,
            partial=False
        ),
        fcn(_motion.Pose):              _schema.motion.pose.PoseSchema(
            many=False,
            partial=False
        ),
        fcn(_motion.PoseList):          _schema.motion.pose.PoseSchema(
            many=True,
            partial=False
        ),
        fcn(_motion.pattern.Pattern):   _schema.motion.pattern.PatternSchema(
            many=False,
            partial=False
        ),
    }

    def encode(self, obj: object, *args, **kwargs) -> AnyStr:
        try:
            # try to dump the data into a string
            return self._MAPPING[fcn(obj)].dumps(obj, *args, **kwargs)
        except KeyError:
            raise NotImplementedError

    def decode(self, stream: AnyStr, *args, **kwargs) -> object:
        # convert stream given as string to a dict
        obj = json.loads(stream)

        # loop over each mapping and try each one till we have a successful
        # decoding, then return that result
        for c, s in self._MAPPING.items():
            try:
                # and load data
                return s.load(obj, *args, **kwargs)
            except Exception as e:
                if isinstance(e.args[0], str):
                    raise e
                print(e)
                pass

        raise TypeError('Could not resolve type of stream given')
