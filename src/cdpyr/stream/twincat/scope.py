from __future__ import annotations

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
    _meta: _meta.ScopeMeta
    _signals: _signal.SignalList

    def __init__(self,
                 signals: Union[
                     _signal.SignalList,
                     Tuple[_signal.Signal],
                     Tuple[Dict[AnyStr, Any]]],
                 meta: Union[_meta.ScopeMeta, Dict[AnyStr, Any]]):
        self._signals = _signal.SignalList(
                [_signal.Signal(**signal) for signal in signals] \
                    if isinstance(signals[0], Dict) \
                    else signals)
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
    def values(self):
        return _np.asarray([signal.values for signal in self._signals])

    __repr__ = make_repr(
            'signals',
            'meta',
    )


__all__ = [
        'Scope'
]
