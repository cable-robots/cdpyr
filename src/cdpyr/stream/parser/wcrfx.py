import functools
import itertools
import operator
import re
from collections import OrderedDict
from typing import AnyStr, Iterable, Mapping, Sequence, Tuple, Union

import fastnumbers
import numpy as _np
import xmltodict

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.stream.parser import parser

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__version__ = '1.0.0-dev'
__status__ = 'Prototype'


def dict_get(m: Mapping, k: Iterable, *args):
    # set keys which are integers to their integer value
    try:
        return functools.reduce(operator.getitem, k, m)
    except (IndexError, TypeError, KeyError) as e:
        if len(args):
            return args[0]
        raise e


class Wcrfx(parser.Parser):
    VERSION = '0.31'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._PROCESSORS = {
                'robot':       {'dump': self._process_dump_robot, },
                'models':      {'load': self._process_load_models, },
                '@id':         {'load': self._process_load_numeric},
                '@x':          {'load': self._process_load_numeric},
                '@y':          {'load': self._process_load_numeric},
                '@z':          {'load': self._process_load_numeric},
                '@a11':        {'load': self._process_load_numeric},
                '@a12':        {'load': self._process_load_numeric},
                '@a13':        {'load': self._process_load_numeric},
                '@a21':        {'load': self._process_load_numeric},
                '@a22':        {'load': self._process_load_numeric},
                '@a23':        {'load': self._process_load_numeric},
                '@a31':        {'load': self._process_load_numeric},
                '@a32':        {'load': self._process_load_numeric},
                '@a33':        {'load': self._process_load_numeric},
                '@Ixx':        {'load': self._process_load_numeric},
                '@Ixy':        {'load': self._process_load_numeric},
                '@Ixz':        {'load': self._process_load_numeric},
                '@Iyx':        {'load': self._process_load_numeric},
                '@Iyy':        {'load': self._process_load_numeric},
                '@Iyz':        {'load': self._process_load_numeric},
                '@Izx':        {'load': self._process_load_numeric},
                '@Izy':        {'load': self._process_load_numeric},
                '@Izz':        {'load': self._process_load_numeric},
                '@radius':     {'load': self._process_load_numeric},
                '@elasticity': {'load': self._process_load_numeric},
                '@mass':       {'load': self._process_load_numeric},
                '@weight':     {'load': self._process_load_numeric},
                '@max_length': {'load': self._process_load_numeric},
                '@damping':    {'load': self._process_load_numeric},
        }

    def kwargs(self, o: RobotComponent, **kwargs):
        return super().kwargs(o, root=o.__class__.__name__.lower(), **kwargs)

    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        # get the root type we are dealing with, pre-process the dictionary,
        # and dump it
        return xmltodict.unparse(
                self._process_dump(kwargs.pop('root', 'root'), d), pretty=True,
                short_empty_elements=True)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        # first, parse from XML to dictionary
        d = xmltodict.parse(s,
                            force_list=('dcm', 'angular', 'linear', 'position'),
                            postprocessor=self._process_load)
        # then, since there always must be a root object in XML, we will
        # strip this off the dictionary from here
        return d[list(d.keys())[0]]

    def _process_dump(self, root: str, o: Union[OrderedDict, Mapping]):
        return self._PROCESSORS[root]['dump'](o)

    def _process_load(self, path: Sequence[Tuple[AnyStr, object]], key: str,
                      value):
        try:
            return self._PROCESSORS[key]['load'](path, key, value)
        except KeyError as KeyE:
            return key, value

    def _process_dump_robot(self, o: Union[OrderedDict, Mapping]):

        def dump_motion_pattern(motion_pattern):
            translation = dict_get(motion_pattern, ('translation',), None)
            rotation = dict_get(motion_pattern, ('rotation',), None)
            return '{R}{T}'.format(R=f'{rotation}R' if rotation else '',
                                   T=f'{translation}T' if translation else '')

        motion_pattern = dump_motion_pattern(
                dict_get(o, ('platforms', 0, 'motion_pattern')))

        xmlo = OrderedDict((
                ('models', OrderedDict((
                        ('@version', self.VERSION),
                        ('robot', OrderedDict((
                                (
                                        '@name',
                                        dict_get(o, ('name',), 'default')),
                                ('@id', ''),
                                ('@author',
                                 dict_get(o, ('author',), __author__)),
                                ('@description',
                                 dict_get(o, ('description',), '')),
                                ('@generator', 'CDPyR Stream to WCRFX'),
                                ('@motionpattern', motion_pattern),
                                ('geometry', OrderedDict((
                                        ('chain', []),))),
                                ('platform', []),
                                ('controller', None),))),
                        ('cable', []),
                        ('winch', []),
                ))),
        ))

        # from the kinematic chains, we will build the robot mode
        for idx, chain in enumerate(o['kinematic_chains']):
            # get references to the linked components
            frame_anchor = o['frame']['anchors'][chain['frame_anchor']]
            platform = o['platforms'][chain['platform']]
            platform_anchor = platform['anchors'][chain['platform_anchor']]
            cable = o['cables'][chain['cable']]

            # append the active `base` element
            xmlo['models']['robot']['geometry']['chain'].append(
                    OrderedDict((
                            ('@id', idx),
                            ('@platform_id', chain['platform'] + 1),
                            ('@cable_id', chain['cable'] + 1),
                            ('@winchtype', 'IPAnema-Winch'),
                            ('base', OrderedDict(itertools.chain(
                                    zip((f'@{c}' for c in 'xyz'),
                                        dict_get(frame_anchor,
                                                 ('position',),
                                                 [0.0, 0.0, 0.0])),
                                    zip((f'@a{r}{c}' for r in [1, 2, 3] for
                                         c in [1, 2, 3]), itertools.chain(
                                            *dict_get(frame_anchor, ('dcm',),
                                                      _np.eye(3)))),
                                    zip(('@radius', ), (dict_get(frame_anchor, ('pulley', 'radius'), 0.0), ))
                            ))),
                            ('platform', OrderedDict(itertools.chain(
                                    zip((f'@{c}' for c in 'xyz'),
                                        dict_get(platform_anchor,
                                                 ('position',),
                                                 [0.0, 0.0, 0.0])),
                                    zip((f'@a{r}{c}' for r in [1, 2, 3] for
                                         c in [1, 2, 3]), itertools.chain(
                                            *dict_get(platform_anchor, ('dcm',),
                                                      _np.eye(3)))),
                            ))),
                    )))

            # create append the `platform` element
            platform = OrderedDict((
                    ('@id', dict_get(chain, ('platform',))),
                    ('@name', dict_get(platform, ('name',))),
                    ('@mass',
                     dict_get(platform, ('inertia', 'linear', 0, 0))),
                    ('@motionpattern', dump_motion_pattern(
                            dict_get(platform, ('motion_pattern',)))),
                    ('inertiatensor', OrderedDict((
                            zip(
                                    (f'@I{r}{c}' for r in ('x', 'y', 'z')
                                     for c in ('x', 'y', 'z')),
                                    itertools.chain(*dict_get(platform, (
                                            'inertia', 'angular'),
                                                              _np.full((3, 3),
                                                                       _np.Infinity))))
                    ))),
                    ('centerofgravity', OrderedDict(zip(('@x', '@y', '@z'),
                                                        dict_get(platform, (
                                                                'center_of_gravity',),
                                                                 [0.0, 0.0,
                                                                  0.0])))),
            ))
            try:
                xmlo['models']['robot']['platform'].index(platform)
            except ValueError:
                xmlo['models']['robot']['platform'].append(platform)

            # append the `cable` element
            xmlo['models']['cable'].append(OrderedDict((
                    ('@id', chain['cable']),
                    ('@name', dict_get(cable, ('name',))),
                    ('@elasticity',
                     dict_get(cable, ('modulus', 'elasticities', 0),
                              _np.Infinity)),
                    ('@radius', 2 * dict_get(cable, ('radius',), 0)),
                    ('@breaking_load', dict_get(cable, ('breaking_load',))),
                    ('@material', dict_get(cable, ('material',)))
            )))

        return xmlo

    def _process_load_numeric(self, path: Sequence[Tuple[AnyStr, object]],
                              key: str, value: OrderedDict):
        return key, fastnumbers.fast_real(value)

    def _process_load_models(self, path: Sequence[Tuple[AnyStr, object]],
                             key: str, value: OrderedDict):
        # store new frame anchors, platforms, platform anchors, cables,
        # and chains in these ordered dicts
        robot = OrderedDict((
                ('name', dict_get(value, ('robot', '@name',))),
                ('frame', OrderedDict((
                        ('anchors', []),
                ))),
                ('platforms', []),
                ('cables', []),
                ('kinematic_chains', [])
        ))

        # create a motion pattern matching regular expression
        motion_pattern_re = re.compile('(?P<r>[123])?R?(?P<t>[123])T')

        def make_motion_pattern(cand):
            match = motion_pattern_re.findall(cand) or [0, 0]
            return OrderedDict((
                    ('translation', match[0][1] if match[0][1] else 0),
                    ('rotation', match[0][0] if match[0][0] else 0)
            ))

        # get the global motion pattern
        global_motion_pattern = make_motion_pattern(
                dict_get(value, ('robot', '@motionpattern'), None))

        # loop over all kinematic chains
        for chain in dict_get(value, ('robot', 'geometry', 'chain')):
            # add the frame anchor
            frame_anchor = OrderedDict((
                    ('position',
                     [dict_get(chain, ('base', f'@{c}'), 0.0) for c in 'xyz']),
                    ('dcm', [[dict_get(chain, ('base', f'@a{r}{c}'),
                                       1.0 if r == c else 0.0) for c in
                              (1, 2, 3)] for r in (1, 2, 3)]),
            ))
            try:
                frame_anchor['pulley'] = OrderedDict((
                        ('radius', dict_get(chain, ('base', '@radius')))
                ))
            except KeyError:
                pass
            robot['frame']['anchors'].append(frame_anchor)
            frame_anchor_index = robot['frame']['anchors'].index(frame_anchor)

            # get the platform or create it
            try:
                platform_dict = dict_get(value, ('robot', 'platform', int(
                        dict_get(chain, ('@platform_id',))) - 1))
            except (TypeError, KeyError, IndexError):
                platform_dict = dict_get(value, ('robot', 'platform'))
            try:
                motion_pattern = make_motion_pattern(
                        dict_get(platform_dict, ('@motionpattern',)))
            except (TypeError, KeyError, IndexError):
                motion_pattern = global_motion_pattern
            platform = OrderedDict((
                    ('motion_pattern', motion_pattern),
                    ('name', dict_get(platform_dict, ('@name',))),
                    ('inertia', OrderedDict((
                            ('linear',
                             [[dict_get(platform_dict, ('@mass',), 1), 0, 0],
                              [0, dict_get(platform_dict, ('@mass',), 1), 0],
                              [0, 0, dict_get(platform_dict, ('@mass',), 1)]]),
                            ('angular', [[dict_get(platform_dict, (
                                    'inertiatensor', f'@I{r}{c}'),
                                                   1.0 if r == c else 0.0) for c
                                          in ('x', 'y', 'z')] for r in
                                         ('x', 'y', 'z')]),))),
                    ('anchors', []),
            ))
            # TODO this finds less platforms than there are because 'anchors'
            #  of the previous platform is non-empty so even if the platform
            #  is the same (but yet without anchors) it will not find it thus
            #  always appending the next platforms
            try:
                platform_index = robot['platforms'].index(platform)
            except ValueError:
                robot['platforms'].append(platform)
                platform_index = 0

            # add
            platform_anchor = OrderedDict((
                    ('position',
                     [dict_get(chain, ('platform', f'@{c}'), 0.0) for c in
                      'xyz']),
                    ('dcm', [[dict_get(chain, ('platform', f'@a{r}{c}'),
                                       1.0 if r == c else 0.0) for c in
                              (1, 2, 3)] for r in (1, 2, 3)]),
            ))
            robot['platforms'][platform_index]['anchors'].append(
                    platform_anchor)
            platform_anchor_index = len(
                    robot['platforms'][platform_index]['anchors']) - 1

            try:
                cable_dict = dict_get(value, (
                        'cable', int(dict_get(chain, ('@cable_id',))) - 1))
            except (TypeError, KeyError, IndexError):
                cable_dict = dict_get(value, ('cable',))
            robot['cables'].append(OrderedDict((
                    ('name', dict_get(cable_dict, ('@name',))),
                    ('modulus', OrderedDict((
                            ('elasticities',
                             dict_get(cable_dict, '@elasticity', None)),
                            ('viscosities',
                             dict_get(cable_dict, '@damping', None)),))),
                    ('diameter', 2 * dict_get(cable_dict, ('@radius',), 0)),
                    ('material', dict_get(cable_dict, ('@material',), None)),
                    ('breaking_load',
                     dict_get(cable_dict, ('@breaking_load',), _np.Infinity)),
            )))
            cable_index = len(robot['cables']) - 1

            robot['kinematic_chains'].append(OrderedDict((
                    ('frame_anchor', frame_anchor_index),
                    ('platform', platform_index),
                    ('platform_anchor', platform_anchor_index),
                    ('cable', cable_index),
            )))

        return key, robot


__all__ = [
        'Wcrfx'
]
