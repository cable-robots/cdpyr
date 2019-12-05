import functools
import itertools
import operator
from collections import OrderedDict, Sequence
from typing import AnyStr, Iterable, Mapping, Union

import numpy as _np
import xmltodict
from cdpyr.stream.parser import parser

from cdpyr.robot.robot_component import RobotComponent

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def kwargs(self, o: RobotComponent, **kwargs):
        return super().kwargs(o, root=o.__class__.__name__.lower(), **kwargs)

    def dumps(self, d: Union[OrderedDict, dict], *args, **kwargs) -> AnyStr:
        # get the root type we are dealing with
        root = kwargs.pop('root', 'root')
        # pre-process the dict
        d = self._preprocess_dump(root, d)
        # now dump
        return xmltodict.unparse(d, pretty=True, short_empty_elements=True)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, dict]:
        raise NotImplementedError()

    def _preprocess_dump(self, t: str, o: Union[Sequence, OrderedDict, dict]):
        if t == 'robot':
            xmlo = OrderedDict((
                    ('models', OrderedDict((
                            ('@version', self.VERSION),
                            ('robot', OrderedDict((
                                    (
                                    '@name', dict_get(o, ('name',), 'default')),
                                    ('@id', ''),
                                    ('@author',
                                     dict_get(o, ('author',), __author__)),
                                    ('@description',
                                     dict_get(o, ('description',), '')),
                                    ('@generator', 'CDPyR Stream to WCRFX'),
                                    ('@motionpattern', dict_get(t, (
                                    'platforms', '0', 'motionpattern', 'human'),
                                                                'None')),
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

                # create the `base` element
                xmlo['models']['robot']['geometry']['chain'].append(
                        OrderedDict((
                                ('@id', idx),
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

                xmlo['models']['robot']['platform'].append(OrderedDict((
                        ('@id', dict_get(chain, ('platform',))),
                        ('@name', dict_get(platform, ('name',))),
                        ('@mass',
                         dict_get(platform, ('inertia', 'linear', 0, 0))),
                        ('inertiatensor', OrderedDict((
                                zip(
                                        (f'@I{r}{c}' for r in ('x', 'y', 'z')
                                         for c in ('x', 'y', 'z')),
                                        itertools.chain(*dict_get(platform, (
                                        'inertia', 'angular'), _np.full((3, 3),
                                                                        _np.Infinity))))
                        ))),
                        ('centerofgravity', OrderedDict(zip(('@x', '@y', '@z'),
                                                            dict_get(platform, (
                                                            'center_of_gravity',),
                                                                     [0.0, 0.0,
                                                                      0.0])))),
                )))

                # create the `cable` element
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

        else:
            raise NotImplementedError()

        return xmlo


__all__ = [
        'Wcrfx'
]
