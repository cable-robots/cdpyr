import _datetime as _datetime
import pathlib as _pl
import re
from enum import Enum, auto
from typing import Any, AnyStr, List, Union

import more_itertools
import pint as _pint
import string_utils

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

_ureg = _pint.UnitRegistry()

re_name_unit = re.compile('^(?P<key>[A-Za-z\-]+)(\[(?P<unit>[a-z]+)\])?$')


def process_header_time_record(values):
    try:
        dt = _datetime.datetime.strptime(' '.join(values[1:]),
                                         "%A, %d %B, %Y %H:%M:%S")
    except ValueError:
        dt = ' '.join(values)

    return {'timestamp': values[0], 'datetime': dt}


def process_header_file(v: List[Any]):
    try:
        return _pl.Path(v[0])
    except ValueError:
        return v[0]


class ParsingState(Enum):
    READY = auto()
    HEADER = auto()
    SIGNAL_META = auto()
    SIGNAL_DATA = auto()
    EOF = auto()


class Parser(object):
    HANDLERS = {
            'start_record':  process_header_time_record,
            'file':          process_header_file,
            'name':          lambda v: ''.join(v),
            'net_id':        lambda v: ''.join(v),
            'symbol_based':  bool,
            'index_group':   int,
            'index_offset':  int,
            'port':          int,
            'variable_size': int,
            'offset':        int,
            'scale_factor':  float,
            'bit_mask':      lambda x: int(x, base=16) + 0x200,
    }

    def __init__(self, file: Union[AnyStr, _pl.Path], delimiter="\t"):
        self.file = file if isinstance(file, _pl.Path) else _pl.Path(
                file).resolve()
        self.delimiter = delimiter
        self._states = iter((ParsingState.READY, ParsingState.HEADER,
                             ParsingState.SIGNAL_META, ParsingState.SIGNAL_DATA,
                             ParsingState.EOF))
        self._state = next(self._states)
        self._data = {}

    def parse(self):
        # read file
        csv = self.file.read_text().split("\n")

        # store processed scope meta data and signals
        self._data = {'meta': {}, 'signals': {}}

        self._state = next(self._states)

        # loop over the file lines while looking forward into the file
        for current_line, next_line in more_itertools.pairwise(csv):
            # completely skip empty lines
            if current_line == '':
                continue

            if self._state == ParsingState.HEADER:
                self._parse_header(current_line)
            elif self._state == ParsingState.SIGNAL_META:
                self._parse_signal_meta(current_line)
            elif self._state == ParsingState.SIGNAL_DATA:
                self._parse_signal_data(current_line)

            if current_line != '' and next_line == '':
                self._state = next(self._states)

            # we reached the implemented file end, so it's safe to bail out here
            if current_line == 'EOF':
                break

        self._data['signals'] = tuple(self._data['signals'].values())
        return self._data

    def _parse_header(self, line: str):
        line_data = line.split(self.delimiter)
        key = self._prepare_cell_key(line_data[0])
        values = line_data[1:]
        try:
            self._data['meta'][key] = self.HANDLERS[key](values)
        except KeyError:
            self._data['meta'][key] = (' '.join(values)).rstrip()

    def _parse_signal_meta(self, line: str):
        line_data = line.split(self.delimiter)
        key = self._prepare_cell_key(line_data[0])
        values = (v for v in line_data[1:-1:2])
        re_match = re_name_unit.match(key)
        try:
            key = self._prepare_cell_key(re_match.group('key'))
            unit = re_match.group('unit')
        except AttributeError:
            unit = None

        for idx, value in enumerate(values):
            try:
                value = self.HANDLERS[key](value)
            except KeyError:
                pass
            try:
                value = _ureg.parse_expression(f'{value} {unit}')
            except _pint.UndefinedUnitError:
                pass
            try:
                self._data['signals'][idx]['meta'][key] = value
            except KeyError:
                self._data['signals'][idx] = {'meta': {key: value}}

    def _parse_signal_data(self, line: str):
        line_data = line.split(self.delimiter)

        # TwinCAT writes a line of tab-separated empty strings between the
        # last data set and the EOF indicator. thus we need to check if the
        # stripped keys all are valid. if not, we will skip the row
        if line_data[0].strip() == '':
            return

        keys = (self._prepare_cell_key(k) for k in line_data[0:-1:2])
        values = (k.strip() for k in line_data[1:-1:2])

        for idx, key_value in enumerate(zip(keys, values)):
            key, value = key_value
            try:
                value = float(value)
            except ValueError:
                pass
            try:
                key = int(key)
            except ValueError:
                pass
            try:
                self._data['signals'][idx]['time'].append(key)
                self._data['signals'][idx]['values'].append(value)
            except AttributeError:
                self._data['signals'][idx] = {'time': [key], 'value': [value]}
            except KeyError:
                self._data['signals'][idx]['time'] = [key]
                self._data['signals'][idx]['value'] = [value]

    def _prepare_cell_key(self, k: str):
        # remove dashes/hyphens and turn camel case into snake case
        return string_utils.camel_case_to_snake(k.strip().replace('-', ''))
