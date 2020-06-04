from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Polyhedron',
]

from collections import abc
from typing import Union

import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry import primitive as _geometry
from cdpyr.geometry._subdivision import subdivide
from cdpyr.typing import Matrix, Vector


class Polyhedron(_geometry.Primitive, abc.Collection):
    """
    (N,3) matrix of faces of the polyhedron sorted in counter-clockwise manner
    """
    _faces: Matrix
    """
    (N,) array of surfaces of each triangle
    """
    _surface_areas: Vector
    """
    (N,3) array of spatial absolute coordinates of the polyhedron vertices
    i.e., points
    """
    _vertices: Matrix
    """
    (N, ) vector of the volumes per tetrahedron
    """
    _volumes: Vector

    VERTICES_OCTAHEDRON = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
    ]

    FACES_OCTAHEDRON = [
            [0, 1, 2],
            [1, 3, 2],
            [3, 4, 2],
            [4, 0, 2],
            [0, 1, 5],
            [1, 3, 5],
            [3, 4, 5],
            [4, 0, 5],
    ]

    def __init__(self, vertices: Matrix, faces: Matrix, center: Vector = None,
                 **kwargs):
        super().__init__(center=center, **kwargs)
        self._vertices = _np.asarray(vertices)
        self._faces = _np.asarray(faces, dtype=_np.uint)
        self._surface_areas = None
        self._volumes = None

    @staticmethod
    def from_octahedron(depth: int = 0, center: Vector = None,
                        fresh: bool = False):
        """
        This function takes the unit octahedron and splits it as many times
        as the user wants to return a polyhedron with unit vertices

        Parameters
        ----------
        depth : int
            Number of splits to perform. Must be greater or equal to zero. If
            zero, the unit octahedron will be returned.
        center : Vector
            Center of the initial octahedron if not `(0.0, 0.0, 0.0)`.
        fresh : bool
            Whether to calculate the values fresh or use possibly
            pre-calculated values from `DATADIR`

        Returns
        -------
        hedron : Polyhedron
            The split octahedron object

        """

        # default center
        center = _np.asarray(center if center is not None else [0.0, 0.0, 0.0])
        if center.ndim == 0:
            center = _np.asarray([center])

        # initial corners and faces from the global constant
        vertices = tuple(
                tuple(vertex) for vertex in Polyhedron.VERTICES_OCTAHEDRON)
        faces = tuple(tuple(face) for face in Polyhedron.FACES_OCTAHEDRON)

        # subdivide triangles into smaller ones using LOOP-SUBDIVISION
        # algorithm_old
        for level in range(depth):
            vertices, faces = subdivide(vertices, faces)

        # convert into numpy arrays
        vertices = _np.asarray(vertices)

        # return a Polyhedron object with the corners shifted by the center
        # given through the user
        return Polyhedron(vertices
                          / _np.linalg.norm(vertices, axis=1)[:, None]
                          + center[None, :], faces)

    @property
    def centroid(self):
        # get vertices sorted by the faces
        vertices = self._vertices[self._faces, :]
        # split up corners
        a = vertices[:, 0, :]
        b = vertices[:, 1, :]
        c = vertices[:, 2, :]

        # calculate the triangles center of mass through its three vertices
        triangle_centroids = _np.sum(vertices, axis=1) / 3
        # surface of each triangle
        triangle_surfaces = 0.5 * _np.linalg.norm(
                _np.cross(a - b, a - c, axis=1), axis=1)

        # the final centroid will be located at the weighted triangles'
        # centroids
        return _np.sum(triangle_surfaces[:, None] * triangle_centroids,
                       axis=0) / _np.sum(triangle_surfaces, axis=0)

    @property
    def faces(self):
        return self._faces

    @property
    def surface_area(self):
        # just sum up over each tetrahedron's surface
        return _np.sum(self.surface_areas, axis=0)

    @property
    def surface_areas(self):
        a = self.vertices[self.faces[:, 0], :]
        b = self.vertices[self.faces[:, 1], :]
        c = self.vertices[self.faces[:, 2], :]

        # heron's formula
        return 0.5 * _np.linalg.norm(_np.cross(a - b, a - c, axis=1), axis=1)

    @property
    def vertices(self):
        return self._vertices

    @property
    def volume(self):
        return _np.sum(self.volumes, axis=0)

    @property
    def volumes(self):
        a = self._vertices[self._faces[:, 0], :]
        b = self._vertices[self._faces[:, 1], :]
        c = self._vertices[self._faces[:, 2], :]
        d = self.centroid

        # Heron's formula
        # | (a - d) . ( (b - d) x (c - d) ) |
        # -----------------------------------
        #                  6
        return _np.abs(
                _np.sum((a - d) * _np.cross(b - d, c - d, axis=1), axis=1)) / 6

    def split(self, depth: int = None):
        """
        Split the current polyhedron into a higher dimensional polyhedron

        Returns
        -------

        """

        # default argument
        if depth is None:
            depth = 1

        # initial corners and faces from the global constant
        vertices = self._vertices - self.center[None, :]
        faces = self.faces

        # subdivide triangles into smaller ones using LOOP-SUBDIVISION
        # algorithm_old
        for level in range(depth):
            vertices, faces = subdivide(vertices, faces)

        # convert into numpy arrays
        vertices = _np.asarray(vertices)

        # update vertices and faces
        self._vertices = vertices / _np.linalg.norm(vertices, axis=1)[:,
                                    None] + self.center[None, :]
        self._faces = _np.asarray(faces, dtype=_np.int64)

    def __iter__(self):
        return zip(self.faces, self.vertices[self.faces, :])

    def __getitem__(self, idx: int):
        return self.vertices[idx, :]

    def __len__(self) -> int:
        try:
            # TODO fix this since it can be that all vertices are the same
            # if any vertex is unequal to zero, we have a length
            return _np.unique(self._vertices, axis=1).shape[0]
        except (IndexError, AttributeError):
            return 0

    def __contains__(self, coordinate: Union[Vector, Matrix]):
        # if there are no coordinates stored, then return `False` right away
        if not len(self):
            return False

        # consistent arguments
        coordinate = _np.asarray(coordinate)

        if coordinate.ndim == 1:
            coordinate = coordinate[None, :]

        try:
            # vector from the coordinate given to each vertex
            diff = self._vertices - coordinate

            # calculate angle between all these differences
            cosine_angles = _np.sum(diff * self._vertices, axis=1) \
                            / _np.linalg.norm(self._vertices, axis=1) \
                            / _np.linalg.norm(diff, axis=1)

            # just in case we divided zero by zero yielding NaN in numpy
            cosine_angles[_np.isnan(cosine_angles)] = 1
        except Exception as e:
            flag = False
        else:
            # all differences are pointing in the same direction as the
            # vertices, if the cosines of the angles are all positive
            flag = (cosine_angles >= 0).all()
        finally:
            return flag

    def __eq__(self, other):
        return super().__eq__(other) \
               and _np.allclose(self._vertices, other.vertices) \
               and _np.allclose(self._faces, other.faces)

    def __hash__(self):
        return hash((self.centroid, self.surface_area, self.volume,
                     self._vertices.shape[0], self._faces.shape[0]))

    __repr__ = make_repr(
            'centroid',
            'surface_area',
            'volume',
            'num_vertices',
            'num_faces',
    )
