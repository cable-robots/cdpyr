from __future__ import annotations

import pathlib as pl
import itertools

import pytest

import cdpyr
import cdpyr.motion.pattern
import cdpyr.stream.parser.parser

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class StreamParserTestSuite(object):

    @pytest.mark.parametrize(
            ('orig', 'parser'),
            itertools.product(
                    (42, 'foo bar', {'foo': 'bar'}, ('foo', 'bar')),
                    (cdpyr.stream.parser.Json(),
                     cdpyr.stream.parser.Xml(),
                     cdpyr.stream.parser.Yaml())),
            ids=list('{}-{}'.format(a, b) for a, b in itertools.product(('num', 'str', 'dict', 'tuple'), ('json', 'xml', 'yaml'))),
    )
    def test_builtin_types(self,
                           orig,
                           parser: cdpyr.stream.parser.parser.Parser,
                           tmpdir: pl.Path):
        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{type(orig).__name__}.{parser.EXT}'

        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        with open(tmpfile, 'r') as f:
            resto = stream.loads(''.join(f.readlines()))

        # compare all data
        assert isinstance(resto, type(orig))
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_pose(self,
                         rand_pose_3r3t: cdpyr.motion.pose.Pose,
                         parser: cdpyr.stream.parser.parser.Parser,
                         tmpdir: pl.Path):
        orig: cdpyr.motion.pose.Pose
        orig = rand_pose_3r3t

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.motion.pose.Pose = stream.loads(''.join(f.readlines()))

        # compare all data
        assert isinstance(resto, cdpyr.motion.pose.Pose)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_motion_pattern(self,
                                   robot_3r3t: cdpyr.robot.Robot,
                                   parser: cdpyr.stream.parser.parser.Parser,
                                   tmpdir: pl.Path):
        orig: cdpyr.motion.pattern.Pattern
        orig = robot_3r3t.platforms[0].motion_pattern

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.motion.pattern.Pattern = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.motion.pattern.Pattern)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_cable(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          parser: cdpyr.stream.parser.parser.Parser,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Cable
        orig = robot_3r3t.cables[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Cable = stream.loads(''.join(f.readlines()))

        assert isinstance(orig, cdpyr.robot.Cable)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_cables(self,
                           robot_3r3t: cdpyr.robot.Robot,
                           parser: cdpyr.stream.parser.parser.Parser,
                           tmpdir: pl.Path):
        orig: cdpyr.robot.CableList
        orig = robot_3r3t.cables

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.CableList = stream.loads(''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.CableList)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_platform_anchor(self,
                                    robot_3r3t: cdpyr.robot.Robot,
                                    parser: cdpyr.stream.parser.parser.Parser,
                                    tmpdir: pl.Path):
        orig: cdpyr.robot.platform.PlatformAnchor
        orig = robot_3r3t.platforms[0].anchors[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.platform.PlatformAnchor = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.platform.PlatformAnchor)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_platform_anchors(self,
                                     robot_3r3t: cdpyr.robot.Robot,
                                     parser: cdpyr.stream.parser.parser.Parser,
                                     tmpdir: pl.Path):
        orig: cdpyr.robot.platform.PlatformAnchorList
        orig = robot_3r3t.platforms[0].anchors

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.platform.PlatformAnchorList = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.platform.PlatformAnchorList)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_frame_anchor(self,
                                 robot_3r3t: cdpyr.robot.Robot,
                                 parser: cdpyr.stream.parser.parser.Parser,
                                 tmpdir: pl.Path):
        orig: cdpyr.robot.frame.FrameAnchor
        orig = robot_3r3t.frame.anchors[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.frame.FrameAnchor = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.frame.FrameAnchor)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_frame_anchors(self,
                                  robot_3r3t: cdpyr.robot.Robot,
                                  parser: cdpyr.stream.parser.parser.Parser,
                                  tmpdir: pl.Path):
        orig: cdpyr.robot.frame.FrameAnchorList
        orig = robot_3r3t.frame.anchors

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.frame.FrameAnchorList = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.frame.FrameAnchorList)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_frame(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          parser: cdpyr.stream.parser.parser.Parser,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Frame
        orig = robot_3r3t.frame

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Frame = stream.loads(''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.Frame)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_platform(self,
                             robot_3r3t: cdpyr.robot.Robot,
                             parser: cdpyr.stream.parser.parser.Parser,
                             tmpdir: pl.Path):
        orig: cdpyr.robot.Platform
        orig = robot_3r3t.platforms[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Platform = stream.loads(''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.Platform)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_platforms(self,
                              robot_3r3t: cdpyr.robot.Robot,
                              parser: cdpyr.stream.parser.parser.Parser,
                              tmpdir: pl.Path):
        orig: cdpyr.robot.PlatformList
        orig = robot_3r3t.platforms

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.PlatformList = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.PlatformList)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_kinematic_chain(self,
                                    robot_3r3t: cdpyr.robot.Robot,
                                    parser: cdpyr.stream.parser.parser.Parser,
                                    tmpdir: pl.Path):
        orig: cdpyr.robot.KinematicChain
        orig = robot_3r3t.kinematic_chains[0]

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.KinematicChain = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.KinematicChain)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'yaml'),
    )
    def test_stream_kinematic_chains(self,
                                     robot_3r3t: cdpyr.robot.Robot,
                                     parser: cdpyr.stream.parser.parser.Parser,
                                     tmpdir: pl.Path):
        orig: cdpyr.robot.KinematicChainList
        orig = robot_3r3t.kinematic_chains

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.KinematicChainList = stream.loads(
                    ''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.KinematicChainList)
        assert resto == orig

    @pytest.mark.parametrize(
            ('parser', ),
            (
                    (cdpyr.stream.parser.Json(), ),
                    (cdpyr.stream.parser.Xml(), ),
                    (cdpyr.stream.parser.Wcrfx(), ),
                    (cdpyr.stream.parser.Yaml(), ),
            ),
            ids=('json', 'xml', 'wcrfx', 'yaml'),
    )
    def test_stream_robot(self,
                          robot_3r3t: cdpyr.robot.Robot,
                          parser: cdpyr.stream.parser.parser.Parser,
                          tmpdir: pl.Path):
        orig: cdpyr.robot.Robot
        orig = robot_3r3t

        # create a JSON stream object
        stream = cdpyr.stream.Stream(parser)

        # file path to save to (with the extension at first)
        tmpfile = tmpdir / f'{orig.__class__.__name__.lower()}.{parser.EXT}'

        # write file with opening the stream first
        with open(tmpfile, 'w') as f:
            f.writelines(stream.dumps(orig))

        # decode the file
        with open(tmpfile, 'r') as f:
            resto: cdpyr.robot.Robot = stream.loads(''.join(f.readlines()))

        assert isinstance(resto, cdpyr.robot.Robot)
        assert resto == orig


if __name__ == "__main__":
    pytest.main()
