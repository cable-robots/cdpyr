import pathlib as pl
import json

import pytest

import cdpyr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class JsonStreamTestSuite(object):

    def test_stream_pose(self,
                         rand_pose_3r3t: cdpyr.motion.Pose,
                         tmpdir: pl.Path):
        orig: cdpyr.motion.Pose = rand_pose_3r3t

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.motion.Pose = stream.decode(f)

        # compare all data
        assert isinstance(resto, cdpyr.motion.Pose)
        assert resto == orig

    def test_stream_motion_pattern(self,
                                   robot_3r3t: cdpyr.robot.Robot,
                                   tmpdir: pl.Path):
        orig: cdpyr.motion.pattern.Pattern = robot_3r3t.platforms[
            0].motion_pattern

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.motion.MotionPattern = stream.decode(f)

        assert isinstance(resto, cdpyr.motion.pattern.Pattern)
        assert resto == orig

    def test_stream_cable(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Cable = robot_3r3t.cables[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Cable = stream.decode(f)

        assert isinstance(orig, cdpyr.robot.Cable)
        assert resto == orig

    def test_stream_cables(self,
                           robot_3r3t: cdpyr.robot.Robot,
                           tmpdir: pl.Path):
        orig: cdpyr.robot.CableList = robot_3r3t.cables

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.CableList = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.CableList)
        assert resto == orig

    def test_stream_platform_anchor(self,
                                    robot_3r3t: cdpyr.robot.Robot,
                                    tmpdir: pl.Path):
        orig: cdpyr.robot.PlatformAnchor = robot_3r3t.platforms[0].anchors[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.PlatformAnchor = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.PlatformAnchor)
        assert resto == orig

    def test_stream_platform_anchors(self,
                                     robot_3r3t: cdpyr.robot.Robot,
                                     tmpdir: pl.Path):
        orig: cdpyr.robot.PlatformAnchorList = robot_3r3t.platforms[0].anchors

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.PlatformAnchorList = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.PlatformAnchorList)
        assert resto == orig

    def test_stream_frame_anchor(self,
                                 robot_3r3t: cdpyr.robot.Robot,
                                 tmpdir: pl.Path):
        orig: cdpyr.robot.FrameAnchor = robot_3r3t.frame.anchors[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.FrameAnchor = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.FrameAnchor)
        assert resto == orig

    def test_stream_frame_anchors(self,
                                  robot_3r3t: cdpyr.robot.Robot,
                                  tmpdir: pl.Path):
        orig: cdpyr.robot.FrameAnchorList = robot_3r3t.frame.anchors

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.FrameAnchorList = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.FrameAnchorList)
        assert resto == orig

    def test_stream_frame(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Frame = robot_3r3t.frame

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Frame = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.Frame)
        assert resto == orig

    def test_stream_platform(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Platform = robot_3r3t.platforms[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Platform = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.Platform)
        assert resto == orig

    def test_stream_platforms(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.PlatformList = robot_3r3t.platforms

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.PlatformList = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.PlatformList)
        assert resto == orig

    def test_stream_kinematic_chain(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.KinematicChain = robot_3r3t.kinematic_chains[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.KinematicChain = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.KinematicChain)
        assert resto == orig

    def test_stream_kinematic_chains(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.KinematicChainList = robot_3r3t.kinematic_chains

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.KinematicChainList = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.KinematicChainList)
        assert resto == orig

    def test_stream_robot(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Robot = robot_3r3t

        # create a JSON stream object
        stream = cdpyr.stream.Stream(cdpyr.stream.parser.JSON())

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / 'asd.json'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            assert stream.encode(orig, f)

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Robot = stream.decode(f)

        assert isinstance(resto, cdpyr.robot.Robot)
        assert resto == orig


__all__ = [
    'JsonStreamTestSuite',
]
