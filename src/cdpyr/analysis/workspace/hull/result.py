from collections import abc

import numpy as _np

from cdpyr.analysis.workspace import (
    result as _result,
)
from cdpyr.analysis.workspace.grid import calculator as _calculator
from cdpyr.typing import Matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Result(_result.Result, abc.Collection):
    _faces: Matrix
    _vertices: Matrix

    def __init__(self,
                 algorithm: '_calculator.Calculator',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 vertices: Matrix,
                 faces: Matrix):
        super().__init__(algorithm, archetype, criterion)
        self._vertices = _np.asarray(vertices)
        self._faces = _np.asarray(faces)

    @property
    def faces(self):
        return self._faces

    @property
    def vertices(self):
        return self._vertices

    def __iter__(self):
        return ((self._faces[idx, :], self._vertices[idx, :]) for idx in
                range(len(self)))

    def __getitem__(self, idx: int):
        return self._faces[idx, :], self._vertices[idx, :]

    def __len__(self) -> int:
        try:
            return self._faces.shape[0]
        except AttributeError as AttributeException:
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
        except BaseException as BaseError:
            flag = False
        else:
            # all differences are pointing in the same direction as the
            # vertices, if the cosines of the angles are all positive
            flag = (cosine_angles >= 0).all()
        finally:
            return flag


__all__ = [
    'Result',
]
