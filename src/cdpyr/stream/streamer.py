from collections import (
    OrderedDict
)
from typing import (
    AnyStr,
    Union
)

from cdpyr import (
    motion as _motion,
    robot as _robot,
    schema as _schema
)
from cdpyr.helpers import full_classname as fcn
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.stream.parser import parser as _parser

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Streamer(object):
    parser: '_parser.Parser'

    # define the mapping of object type and marshmallow schemes
    _RESOLVER = {
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

    def __init__(self, parser: '_parser.Parser' = None):
        self.parser = parser

    def dump(self, o: RobotComponent, *args, **kwargs):
        """
        Dump a CDPyR component as dictionary

        Parameters
        ----------
        o : RobotComponent

        Returns
        -------
        d : dict
            Dictionary representation of the CDPyR component

        """
        try:
            # try to dump the data
            return self._RESOLVER[fcn(o)].dump(o, *args, **kwargs)
        except KeyError:
            raise ValueError(f'Cannot dump object of type {type(o)}.')

    def dumps(self, o: RobotComponent, *args, **kwargs):
        """
        Dump a CDPyR component as a string

        Parameters
        ----------
        o : RobotComponent

        Returns
        -------
        s : AnyStr
            A string representation of the CDPyR component in the parser's
            configured format

        """

        # for convenience with some parsers, we will pass the root object's
        # type along to the `dumps` method
        kwargs = self.parser.kwargs(o, **kwargs)

        # turn the object into a dictionary and then dump this to the right
        # format
        return self.parser.dumps(self.dump(o), *args, **kwargs)

    def load(self, d: Union[OrderedDict, dict], *args, **kwargs):
        """
        Load dictionary into the CDPyR compatible objects
        Parameters
        ----------
        d : OrderedDict | dict
            Dictionary representing the CDPyR component

        Returns
        -------
        o : RobotComponent
            The matching

        Raises
        ------
        TypeError
            Raises an exception of the object could not be converted

        """
        # loop over each mapping and try each one till we have a successful
        # decoding, then return that result
        for c, s in self._RESOLVER.items():
            try:
                # and load data
                return s.load(d, *args, **kwargs)
            except Exception as e:
                if isinstance(e.args[0], str):
                    raise e
                pass

        raise TypeError('Could not resolve type of stream given.')

    def loads(self, s: AnyStr, *args, **kwargs):
        """
        Load a string into a CDPyR component

        Parameters
        ----------
        s : AnyStr

        Returns
        -------
        o : RobotComponent
            The parsed robot component as a CDPyR component

        Raises
        ------
                TypeError
            Raises an exception of the object could not be converted

        """
        return self.load(self.parser.loads(s), *args, **kwargs)
