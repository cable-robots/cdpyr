from __future__ import annotations

from collections import OrderedDict
from typing import AnyStr, IO

import cdpyr.schema.robot.anchor
from cdpyr import motion as _motion, robot as _robot, schema as _schema
from cdpyr.base import CdpyrObject
from cdpyr.helpers import full_classname as fcn
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.stream.parser import parser as _parser

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Stream(CdpyrObject):
    parser: _parser.Parser

    # define the mapping of object type and marshmallow schemes
    _RESOLVER = {
            fcn(_robot.Cable):
                _schema.robot.CableSchema(
                        many=False,
                        partial=False),
            fcn(_robot.CableList):
                _schema.robot.CableSchema(
                        many=True,
                        partial=False),
            fcn(_robot.Drum):
                _schema.robot.DrumSchema(
                        many=False,
                        partial=False),
            fcn(_robot.Drivetrain):
                _schema.robot.DriveTrainSchema(
                        many=False,
                        partial=False),
            fcn(_robot.Frame):
                _schema.robot.FrameSchema(
                        many=False,
                        partial=False),
            fcn(_robot.FrameAnchor):
                _schema.robot.FrameAnchorSchema(
                        many=False,
                        partial=False),
            fcn(_robot.FrameAnchorList):
                _schema.robot.FrameAnchorSchema(
                        many=True,
                        partial=False),
            fcn(_robot.Gearbox):
                _schema.robot.GearboxSchema(
                        many=False,
                        partial=False),
            fcn(_robot.KinematicChain):
                _schema.robot.KinematicChainSchema(
                        many=False,
                        partial=False),
            fcn(_robot.KinematicChainList):
                _schema.robot.KinematicChainSchema(
                        many=True,
                        partial=False),
            fcn(_robot.Motor):
                _schema.robot.MotorSchema(
                        many=False,
                        partial=False),
            fcn(_robot.Platform):
                _schema.robot.PlatformSchema(
                        many=False,
                        partial=False),
            fcn(_robot.PlatformList):
                _schema.robot.PlatformSchema(
                        many=True,
                        partial=False),
            fcn(_robot.PlatformAnchor):
                _schema.robot.PlatformAnchorSchema(
                        many=False,
                        partial=False),
            fcn(_robot.PlatformAnchorList):
                _schema.robot.PlatformAnchorSchema(
                        many=True,
                        partial=False),
            fcn(_robot.Pulley):
                _schema.robot.PulleySchema(
                        many=False,
                        partial=False),
            fcn(_robot.Robot):
                _schema.robot.RobotSchema(
                        many=False,
                        partial=False),
            fcn(_motion.pose.Pose):
                _schema.motion.pose.PoseSchema(
                        many=False,
                        partial=False),
            fcn(_motion.pose.PoseList):
                _schema.motion.pose.PoseSchema(
                        many=True,
                        partial=False),
            fcn(_motion.pattern.Pattern):
                _schema.motion.pattern.PatternSchema(
                        many=False,
                        partial=False),
    }

    def __init__(self, parser: _parser.Parser, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    def dump(self, f: IO, o: RobotComponent, *args, **kwargs):
        """

        Parameters
        ----------
        f : IO
            A file-like object that supports :code:`write()` and
            :code:`writelines()`.
        o : object
            Any object type or robot component object
        args
        kwargs

        Returns
        -------

        """

        # now we should have a `dict`-like object, so we'll just let the
        # explicit parser implementation take care of converting the object into
        # the correct string-representation
        f.write(self.dumps(o, *args, **kwargs))

    def dumps(self, o: RobotComponent, *args, **kwargs):
        """
        Dump a robot component into a string-like object

        Parameters
        ----------
        o : RobotComponent
            A robot component to convert into a string-like object
        args
        kwargs

        Returns
        -------

        """
        # first, convert `o` into a dictionary
        try:
            o = self._RESOLVER[fcn(o)].dump(o)
        except KeyError:
            pass

        # let the parser handle turning the dictionary into its representation
        return self.parser.dumps(o, *args, **kwargs)

    def load(self, f: IO, *args, **kwargs):
        """
        Load a robot component or other data type from a file-like object

        Parameters
        ----------
        f : IO
            A file-like object that supports :code:`read()` and
            :code:`readlines()`.
        args
        kwargs

        Returns
        -------
        o : object, RobotComponent
            Either an object of built-in type or a RobotComponent object
        """
        return self.loads(''.join(f.readlines()), *args, **kwargs)

    def loads(self, s: AnyStr, *args, **kwargs):
        """
        Load a robot component or other data type from a string-like object

        Parameters
        ----------
        s
        args
        kwargs

        Returns
        -------

        """
        # first, let the parser convert the string into a valid python object
        # (dictionary or alike)
        o = self.parser.loads(s, *args, **kwargs)

        # then, loop over each mapping and try each one till we have a
        # successful decoding, then return that result
        for c, s in self._RESOLVER.items():
            try:
                # load data using the Marshmallow schema object
                o = s.load(o, *args, **kwargs)
            except Exception:
                pass

        return dict(o) if isinstance(o, OrderedDict) else o
