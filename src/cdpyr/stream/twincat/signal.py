from __future__ import annotations

from collections import UserList
from typing import Any, AnyStr, Dict, Iterable, List, Optional, Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.stream.twincat import meta as _meta
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Signal(object):
    _data: Matrix
    _meta: _meta.SignalMeta

    def __init__(self,
                 time: Vector,
                 values: Vector,
                 meta: Union[_meta.SignalMeta, Dict[AnyStr, Any]]):
        self._data = _np.vstack([time, values]).T
        self._meta = meta \
            if isinstance(meta, _meta.SignalMeta) \
            else _meta.SignalMeta(**meta)

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
        return self._data[:, 0]

    @property
    def values(self):
        return self._data[:, 1:-1]

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


__all__ = [
        'Signal',
        'SignalList',
]
