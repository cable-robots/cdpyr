from __future__ import annotations

from collections import UserList
from typing import Any, AnyStr, Dict, Iterable, List, Optional, Union

import numpy as _np
import pint as _pint
from magic_repr import make_repr

from cdpyr.stream.twincat import units as _tcunits
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Signal(object):
    _data: Matrix
    _meta: SignalMeta

    def __init__(self,
                 time: Vector,
                 values: Vector,
                 meta: Union[SignalMeta, Dict[AnyStr, Any]]):
        self._data = _np.hstack([_np.asarray(time)[:, None], values])
        self._meta = meta \
            if isinstance(meta, SignalMeta) \
            else SignalMeta(**meta)

    @property
    def bit_mask(self):
        return self._meta.bit_mask

    @property
    def data_type(self):
        return self._meta.data_type

    @property
    def index_group(self):
        return self._meta.index_group

    @property
    def index_offset(self):
        return self._meta.index_offset

    @property
    def meta(self):
        return self._meta

    @property
    def name(self):
        return self._meta.name

    @property
    def net_id(self):
        return self._meta.net_id

    @property
    def offset(self):
        return self._meta.offset

    @property
    def port(self):
        return self._meta.port

    def sampled(self):
        return iter(self._data)

    @property
    def samples(self):
        return self._data[:, 0]

    @property
    def sample_time(self):
        return self._meta.sample_time

    @property
    def scale_factor(self):
        return self._meta.scale_factor

    @property
    def symbol_based(self):
        return self._meta.symbol_based

    @property
    def symbol_name(self):
        return self._meta.symbol_name

    @property
    def symbol_comment(self):
        return self._meta.symbol_comment

    @property
    def time(self):
        return self._data[:, 0] * self.sample_time

    def timed(self):
        return iter(_np.hstack((self.time.magnitude[:, None], self.values)))

    @property
    def values(self):
        return self._data[:, 1:]

    @property
    def variable_size(self):
        return self._meta.variable_size

    def __iter__(self):
        return iter(self._data)

    __repr__ = make_repr(
            'bit_mask',
            'data_type',
            'index_group',
            'index_offset',
            'name',
            'net_id',
            'offset',
            'port',
            'sample_time',
            'scale_factor',
            'symbol_based',
            'symbol_name',
            'symbol_comment',
            'time',
            'values',
            'variable_size',
    )


class SignalList(UserList):
    data: List[Signal]

    def __init__(self, initlist: Optional[Iterable[Any]] = None):
        super().__init__(initlist)

    def __getattr__(self, item, *args, **kwargs):

        try:
            # filter signals by name
            signals = [signal for signal in self.data if signal.name == item]

            # if there are signals matching the name, we will return them as a
            # new `SignalList`
            if signals:
                return SignalList(signals)
        except BaseException:
            pass

        raise AttributeError(f"'SignalList' object has no attribute '{item}'")


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
                 sample_time: Union[Num, _pint.Quantity] = None,
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
        # convert sample time to base units
        try:
            sample_time = sample_time.to_base_units()
        # didn't work, so `sample_time` is no `pint.Quantity` object
        except AttributeError:
            # parse the sample time with or without unit
            sample_time = _tcunits.ureg.Quantity(sample_time)
            # if there is no dimension on the `sample_time`
            if sample_time.dimensionless:
                # append unit `second` as default
                sample_time *= _tcunits.ureg('second')
        # and store parsed sample time
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
        'Signal',
        'SignalList',
        'SignalMeta',
]
