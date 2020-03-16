from __future__ import annotations

import datetime as _datetime
import pathlib as _pl
from typing import AnyStr, Union

import pint as _pint
from magic_repr import make_repr

from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


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


class SignalMeta(object):
    bit_mask: Num
    data_type: str
    index_group: int
    index_offset: int
    name: str
    net_id: str
    offset: int
    port: int
    sample_time: _pint.Quantity
    scale_factor: Num
    symbol_based: bool
    symbol_name: str
    symbol_comment: str
    variable_size: int

    def __init__(self,
                 name: str = None,
                 net_id: str = None,
                 port: int = None,
                 sample_time: _pint.Quantity = None,
                 symbol_based: bool = None,
                 symbol_name: str = None,
                 symbol_comment: str = None,
                 index_group: int = None,
                 index_offset: int = None,
                 data_type: str = None,
                 variable_size: int = None,
                 offset: int = None,
                 scale_factor: Num = None,
                 bit_mask: Num = None):
        self._name = name
        self._net_id = net_id
        self._port = port
        self._sample_time = sample_time
        self._symbol_based = symbol_based
        self._symbol_name = symbol_name
        self._symbol_comment = symbol_comment
        self._index_group = index_group
        self._index_offset = index_offset
        self._data_type = data_type
        self._variable_size = variable_size
        self._offset = offset
        self._scale_factor = scale_factor
        self._bit_mask = bit_mask

    @property
    def bit_mask(self):
        return self._bit_mask

    @property
    def data_type(self):
        return self._data_type

    @property
    def index_group(self):
        return self._index_group

    @property
    def index_offset(self):
        return self._index_offset

    @property
    def name(self):
        return self._name

    @property
    def net_id(self):
        return self._net_id

    @property
    def offset(self):
        return self._offset

    @property
    def port(self):
        return self._port

    @property
    def sample_time(self):
        return self._sample_time

    @property
    def scale_factor(self):
        return self._scale_factor

    @property
    def symbol_based(self):
        return self._symbol_based

    @property
    def symbol_name(self):
        return self._symbol_name

    @property
    def symbol_comment(self):
        return self._symbol_comment

    @property
    def variable_size(self):
        return self._variable_size

    __repr__ = make_repr(
            'name',
            'net_id',
            'port',
            'sample_time',
            'symbol_based',
            'symbol_name',
            'symbol_comment',
            'index_group',
            'index_offset',
            'data_type',
            'variable_size',
            'offset',
            'scale_factor',
            'bit_mask',
    )


__all__ = [
        'ScopeMeta',
        'SignalMeta',
]
