import pathlib as _pl
from typing import Any, AnyStr, Dict, IO, Tuple, Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.stream.twincat import (
    meta as _meta,
    parser as _parser,
    signal as _signal
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Scope(object):
    _meta: '_meta.ScopeMeta'
    _signals: Tuple['_signal.Signal']

    def __init__(self, signals: Tuple['_signal.Signal'],
                 meta: Union['_meta.ScopeMeta', Dict[AnyStr, Any]]):
        self._signals = signals \
            if isinstance(signals[0], _signal.Signal) \
            else [_signal.Signal(**signal) for signal in signals]
        self._meta = meta \
            if isinstance(meta, _meta.ScopeMeta) \
            else _meta.ScopeMeta(**meta)

    @staticmethod
    def from_file(f: Union[AnyStr, _pl.Path, IO], delimiter="\t"):
        return Scope(**_parser.Parser(f, delimiter).parse())

    @property
    def end(self):
        return self._meta.end_record

    @property
    def file(self):
        return self._meta.file

    @property
    def meta(self):
        return self._meta

    @property
    def name(self):
        return self._meta.name

    @property
    def signals(self):
        return self._signals

    @property
    def start(self):
        return self._meta.start_record

    @property
    def time(self):
        return _np.asarray([signal.time for signal in self._signals])

    @property
    def value(self):
        return _np.asarray([signal.value for signal in self._signals])

    def __iter__(self):
        return iter(self._signals)

    __repr__ = make_repr(
            'signals',
            'meta',
    )


__all__ = [
        'Scope'
]
