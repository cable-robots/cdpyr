from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Scope',
        'ScopeMeta',
]

import datetime as _datetime
import pathlib as _pl
from typing import Any, AnyStr, Dict, IO, Tuple, Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.stream.twincat import (
    parser as _tcparser,
    signal as _tcsignal,
)


class Scope(object):
    _meta: ScopeMeta
    _signals: _tcsignal.SignalList

    def __init__(self,
                 signals: Union[
                     _tcsignal.SignalList,
                     Tuple[_tcsignal.Signal],
                     Tuple[Dict[AnyStr, Any]]],
                 meta: Union[ScopeMeta, Dict[AnyStr, Any]]):
        self._signals = _tcsignal.SignalList(
                [_tcsignal.Signal(**signal) for signal in signals]
                if isinstance(signals[0], Dict)
                else signals)
        self._meta = meta \
            if isinstance(meta, ScopeMeta) \
            else ScopeMeta(**meta)

    @staticmethod
    def from_file(f: Union[AnyStr, _pl.Path, IO], delimiter="\t"):
        return Scope(**_tcparser.Parser(f, delimiter).parse())

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

    def __iter__(self):
        return iter(self._signals)

    __repr__ = make_repr(
            'signals',
            'meta',
    )


class ScopeMeta(object):
    _name: str
    _file: Union[AnyStr, _pl.Path]
    _start_record: Union[AnyStr, _datetime.datetime]
    _end_record: Union[AnyStr, _datetime.datetime]

    def __init__(self,
                 name: str,
                 file: Union[AnyStr, _pl.Path],
                 start_record: Union[AnyStr, _datetime.datetime],
                 end_record: Union[AnyStr, _datetime.datetime]):
        self._name = name
        self._file = file
        self._start_record = start_record
        self._end_record = end_record

    @property
    def end_record(self):
        return self._end_record

    @property
    def file(self):
        return self._file

    @property
    def name(self):
        return self._name

    @property
    def start_record(self):
        return self._start_record

    __repr__ = make_repr(
            'name',
            'file',
            'start_record',
            'end_record',
    )
