from __future__ import annotations

import _datetime as _datetime
import pathlib as _pl
from collections import OrderedDict
from typing import Any, AnyStr, Dict, List, Tuple, Union

import case_changer
import more_itertools
import numpy as _np
import pint as _pint
import re
from enum import Enum, auto

from cdpyr.stream.twincat import units as _units
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

# regular expression object to match a symbol name and its unit
reg_name_unit = re.compile('^(?P<key>[A-Za-z\_\-]+)(\[(?P<unit>[a-z]+)\])?$')
# regular expression object to match vector-like names
reg_signal_name = re.compile('^(?P<name>[a-zA-Z\_\.]+)(\[(?P<index>\d+)\])?$')


# callback to parse the "StartRecord" and "EndRecord" header fields
def process_header_time_record(values):
    try:
        dt = _datetime.datetime.strptime(' '.join(values[1:]),
                                         "%A, %d %B, %Y %H:%M:%S")
    except ValueError:
        dt = ' '.join(values)

    return {'timestamp': values[0], 'datetime': dt}


# callback to parse the "File" header field
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
    """

    """

    # handlers for different header fields
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

    # list of sequential states this parser can be in
    STATES = (ParsingState.HEADER,
              ParsingState.SIGNAL_META,
              ParsingState.SIGNAL_DATA,
              ParsingState.EOF,)

    def __init__(self, file: Union[AnyStr, _pl.Path], delimiter="\t"):
        # file path
        self.file = _pl.Path(file).resolve()
        # file delimiter to use
        self.delimiter = delimiter
        # parse data
        self._data = {}

    def parse(self):
        """
        Parse the assigned TwinCAT 3 scope CSV file

        Returns
        -------
        scope : cdpyr.stream.twincat.scope.Scope
            Scope object
        """

        # store processed scope meta data and signals
        self._data = {'meta': dict(), 'signals': OrderedDict()}

        # iterator over all possible states
        states = iter(self.STATES)
        # and the current state is the first/next of all possible states
        state = next(states)

        # loop over the file lines while looking forward into the file
        with open(self.file, 'r') as f:
            # get current and next line for lookahead of changing state
            for current_line, next_line in more_itertools.pairwise(f):
                # strip newline breaks from current and next line
                current_line = current_line.rstrip("\n")
                next_line = next_line.rstrip("\n")

                # completely skip empty lines
                if current_line == '':
                    continue

                # process the current line depending on what state we are in
                if state == ParsingState.HEADER:
                    self._parse_header(current_line)
                elif state == ParsingState.SIGNAL_META:
                    self._parse_signal_meta(current_line)
                elif state == ParsingState.SIGNAL_DATA:
                    self._parse_signal_data(current_line)

                # if the next line is empty and the current is not,
                # we advance to the next state
                if next_line == '' and current_line != '':
                    state = next(states)

                # we reached the implemented file end, so it's safe to bail
                # out here
                if current_line == 'EOF':
                    break

        # merge signals with a vector-like name
        self._data['signals'] = self._merge_signals(
                tuple(self._data['signals'].values()))

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
        values = line_data[1:-1:2]

        # some keys are given as "name[unit]" which we will split into here
        try:
            re_match = reg_name_unit.match(key)
            key = re_match.group('key')
            unit = re_match.group('unit')
        except AttributeError:
            unit = None

        for idx, value in enumerate(values):
            # apply data handler for the field if it exists
            try:
                value = self.HANDLERS[key](value)
            except KeyError:
                pass

            # try to parse the string as a unit, if possible
            try:
                value = _units.ureg.parse_expression(f'{value} {unit}')
            except _pint.UndefinedUnitError:
                pass

            # assign to existing 'meta' dict or create a new one on the first
            # key
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

        # get every data key and (stripped) value
        keys = (self._prepare_cell_key(k) for k in line_data[0::2])
        values = (k.strip() for k in line_data[1::2])

        # loop over each signal
        for idx, key_value in enumerate(zip(keys, values)):
            key, value = key_value

            # try converting into float or integer
            try:
                value = float(value)
            except ValueError:
                pass
            try:
                key = int(key)
            except ValueError:
                pass

            # append the time and value to the list of existing times and
            # values, or create a new dictionary of lists if it doesn't exist
            try:
                self._data['signals'][idx]['time'].append(key)
                self._data['signals'][idx]['values'].append(value)
            except KeyError:
                self._data['signals'][idx]['time'] = [key]
                self._data['signals'][idx]['values'] = [value]

    @staticmethod
    def _prepare_cell_key(k: str):
        # remove dashes/hyphens and turn camel case into snake case
        try:
            return str(int(k))
        except ValueError:
            # check if there's a unit in the key e.g., `SampleTime[ms]`
            if '[' in k:
                idx_unit = k.index('[')
                k, unit = k[:idx_unit], k[idx_unit:]
            else:
                unit = ''
            return case_changer.snake_case(k.strip().replace('-', '')) + unit

    @staticmethod
    def _merge_signals(signals: Tuple[
        Dict[AnyStr, Union[
            Dict[AnyStr, Union[AnyStr, _units.ureg.Quantity, Num]],
            Vector]]]):
        # new signals stored in a dict
        new_signals = {}
        # loop over every signal
        for signal in signals:
            # see if signal matches a 'vector'-name identifier
            reg_match = reg_signal_name.match(signal['meta']['name'])
            # get name and index
            name, index = reg_match.group('name'), reg_match.group('index')
            # append
            try:
                new_signals[name]['values'][index] = signal['values']
            except KeyError:
                # change signal's original `Name` attribute
                signal['meta']['name'] = name
                # also change signal's original `SymbolName` attribute
                signal['meta']['symbol_name'] = signal['meta'][
                    'symbol_name'].replace(f'{name}[{index}]', name)
                # and create a new signal dict
                new_signals[name] = {
                        'time':   signal['time'],
                        'values': OrderedDict({index: signal['values']}),
                        'meta':   signal['meta']
                }

        # sort vector signals by index
        for key, signal in new_signals.items():
            new_signals[key]['values'] = _np.asarray(
                    [signal['values'][index] for index in
                     sorted(signal['values'].keys())]).T


        # return the squeezed data
        return tuple(new_signals.values())
