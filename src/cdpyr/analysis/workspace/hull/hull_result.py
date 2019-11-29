from collections import abc

import numpy as _np

from cdpyr.analysis.workspace import (
    result as _result,
)
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.grid import grid_calculator as _calculator
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class HullResult(_result.Result, abc.Collection):
    _faces: Matrix
    _vertices: Matrix

    def __init__(self,
                 algorithm: '_calculator.GridCalculator',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 vertices: Matrix,
                 faces: Matrix):
        super().__init__(algorithm, archetype, criterion)
        self._faces = _np.asarray(faces)
        self._vertices = _np.asarray(vertices)

    @property
    def faces(self):
        return self._faces

    @property
    def surface(self):
        if self._surface is None:
            # get each vertex
            f0 = self._vertices[self._faces[:, 0], :]
            f1 = self._vertices[self._faces[:, 1], :]
            f2 = self._vertices[self._faces[:, 2], :]

            # length of each side
            a = _np.linalg.norm(f0 - f1, axis=1)
            b = _np.linalg.norm(f1 - f2, axis=1)
            c = _np.linalg.norm(f2 - f0, axis=1)

            # heron's formula
            self._surface = _np.sum(1.0 / 4.0 * _np.sqrt(
                (a ** 2 + b ** 2 + c ** 2) ** 2 - 2 * (
                    a ** 4 + b ** 4 + c ** 4)), axis=0)

        return self._surface

    @property
    def vertices(self):
        return self._vertices

    @property
    def volume(self):
        if self._volume is None:
            # get each vertex
            a = self._vertices[self._faces[:, 0], :]
            b = self._vertices[self._faces[:, 1], :]
            c = self._vertices[self._faces[:, 2], :]
            d = _np.zeros((3,))

            # | (a - d) . ( (b - d) x (c - d) ) |
            # -----------------------------------
            #                  6
            self._volume = _np.sum(_np.abs(
                _np.sum((a - d) * _np.cross(b - d, c - d, axis=1), axis=1))) / 6

        return self._volume

    def __iter__(self):
        return ((self._faces[idx, :], self._vertices[idx, :]) for idx in
                range(len(self)))

    def __getitem__(self, idx: int):
        return self._faces[idx, :], self._vertices[idx, :]

    def __len__(self) -> int:
        try:
            # TODO fix this since it can be that all vertices are the same
            # if any vertex is unequal to zero, we have a length
            return _np.unique(self._vertices, axis=1).shape[0]
        except (IndexError, AttributeError):
            return 0

    def __contains__(self, coordinate: object):
        # if there are no coordinates stored, then return `False` right away
        if not len(self):
            return False

        # consistent arguments
        coordinate = _np.asarray(coordinate)

        if coordinate.ndim == 1:
            coordinate = coordinate[_np.newaxis, :]

        try:
            # vector from the coordinate given to each vertex
            diff = self._vertices - coordinate

            # calculate angle between all these differences
            cosine_angles = _np.sum(diff * self._vertices, axis=1) \
                            / _np.linalg.norm(self._vertices, axis=1) \
                            / _np.linalg.norm(diff, axis=1)

            # just in case we divided zero by zero yielding NaN in numpy
            cosine_angles[_np.isnan(cosine_angles)] = 1

            # # if all these angles are
            # # solve the problem V.x = c where V are all vertices,
            # x are scaling
            # # factors of each vertex, and c is the coordinate to find
            # sol = _np.linalg.lstsq(self._vertices.T, coordinate)
            #
            # # if all solutions are between 0 and 1 and the sum equals 1,
            # then the
            # # coordinate is inside the workspace
            #
            # scales = sol[0]
            #
            # flag = _np.logical_and(0 <= scales, 1 <= scales)
        except BaseException as BaseE:
            flag = False
        else:
            # all differences are pointing in the same direction as the
            # vertices, if the cosines of the angles are all positive
            flag = (cosine_angles >= 0).all()
        finally:
            return flag


__all__ = [
    'HullResult',
]
