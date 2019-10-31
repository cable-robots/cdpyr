from collections import abc

import numpy as _np

from cdpyr.analysis.workspace import (
    result as _result,
)
from cdpyr.analysis.workspace.grid import calculator as _calculator
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(_result.Result, abc.Collection):
    _coordinates: Matrix
    _flags: Vector
    _inside: Matrix
    _outside: Matrix

    def __init__(self,
                 algorithm: '_calculator.Calculator',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 coordinates: Matrix,
                 flags: Vector):
        super().__init__(algorithm, archetype, criterion)
        self._coordinates = _np.asarray(coordinates)
        self._flags = _np.asarray(flags)
        self._inside = None
        self._outside = None

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def flags(self):
        return self._flags

    @property
    def inside(self):
        # no cached result?
        if self._inside is None:
            self._inside = _np.asarray(
                [self._coordinates[idx, :] for idx in range(len(self)) if
                 self._flags[idx]])

        return self._inside

    @property
    def num_coordinates(self):
        return self._coordinates.shape[0]

    @property
    def outside(self):
        # no cached result?
        if self._outside is None:
            self._outside = _np.asarray(
                [self._coordinates[idx, :] for idx in range(len(self)) if
                 not self._flags[idx]])

        return self._outside

    def __iter__(self):
        return ((self._coordinates[idx, :], self._flags[idx]) for idx in
                range(len(self)))

    def __getitem__(self, idx: int):
        return self._coordinates[idx, :], self._flags[idx]

    def __len__(self) -> int:
        try:
            return self._coordinates.shape[0]
        except AttributeError as AttributeException:
            return 0

    def __contains__(self, coordinate: object):
        # if there are no coordinates stored, then return `False` right away
        if not len(self):
            return False

        # consistent arguments
        coordinate = _np.asarray(coordinate)

        # pad coordinate with zeros in case it is shorter than the grid's
        # coordinates
        coordinate = _np.pad(coordinate,
                             (0, self._coordinates[0].size - coordinate.size))
        # find the coordinate that's closest to the given coordinate
        idx = _np.linalg.norm(self._coordinates - coordinate, axis=1).argmin(
            axis=0)

        try:
            return self._flags[idx]
        except KeyError as KeyException:
            return False


__all__ = [
    'Result',
]
