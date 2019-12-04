import itertools

import numpy as _np
from magic_repr import make_repr

from cdpyr.geometry import geometry as _geometry
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Polyhedron(_geometry.Geometry):
    """
    (N,3) matrix of faces of the polyhedron sorted in counter-clockwise manner
    """
    _faces: Matrix
    """
    (N,) array of surfaces of each triangle
    """
    _surfaces: Vector
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

    def __init__(self, vertices: Matrix, faces: Matrix, **kwargs):
        super().__init__(**kwargs)
        self._vertices = _np.asarray(vertices)
        self._faces = _np.asarray(faces)
        self._surfaces = None
        self._volumes = None

    @staticmethod
    def from_octahedron(depth: int = 0, center: Vector = None):
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

        Returns
        -------
        hedron : Polyhedron
            The split octahedron object

        """

        center = _np.asarray(center if center is not None else [0.0, 0.0, 0.0])
        if center.ndim == 0:
            center = _np.asarray([center])

        # internal callback methods
        def _subdivide(vrtcs, fcs):
            new_faces = []
            num_vertices = len(vrtcs)
            dim_vertices = len(vrtcs[0])

            num_vertices_range = list(range(num_vertices))
            dim_vertices_range = list(range(dim_vertices))

            new_vertices = dict(zip(num_vertices_range, vrtcs))

            # matrix that holds which edges are adjacent to another
            edge_vertices = [
                    [
                            [
                                    -1 for kx in dim_vertices_range
                            ]
                            for ky in num_vertices_range
                    ]
                    for kz in num_vertices_range
            ]

            # create matrix of edge-vertices and new vertices
            for face in fcs:
                a, b, c = face
                ab = _add_edge_vertex(a, b, c, edge_vertices)
                bc = _add_edge_vertex(b, c, a, edge_vertices)
                ac = _add_edge_vertex(a, c, b, edge_vertices)

                new_faces.extend([
                        [a, ab, ac],
                        [ab, b, bc],
                        [ac, bc, c],
                        [ac, ab, bc],
                ])

            # position of new vertices
            for v1, v2 in itertools.product(num_vertices_range,
                                            num_vertices_range):
                vNIndex = edge_vertices[v1][v2][0]
                if vNIndex != -1:
                    # catch boundary case
                    if edge_vertices[v1][v2][2] == -1:
                        value = (
                                [0.5 * vrtcs[v1][idx] + vrtcs[v2][idx] for idx
                                 in
                                 dim_vertices_range])
                    else:
                        value = [3 / 8 * (
                                vrtcs[v1][idx] + vrtcs[v2][idx]) + 1 / 8 * (
                                         vrtcs[edge_vertices[v1][v2][1]][idx] +
                                         vrtcs[edge_vertices[v1][v2][2]][idx])
                                 for idx in dim_vertices_range]

                    new_vertices[vNIndex] = value

            # adjacent vertices
            adjacent_vertices = []
            for v, vTmp in itertools.product(num_vertices_range,
                                             num_vertices_range):
                if v < vTmp and edge_vertices[v][vTmp][1] != -1 \
                        or v > vTmp and edge_vertices[vTmp][v][1] != -1:
                    try:
                        adjacent_vertices[v].append(vTmp)
                    except IndexError as IndexE:
                        adjacent_vertices.insert(v, [vTmp])

            for v in num_vertices_range:
                try:
                    k = len(adjacent_vertices[v])
                except IndexError as IndexE:
                    continue

                adjacent_boundary_vertices = []
                for i in range(k):
                    vi = adjacent_vertices[v][i]
                    if vi > v and edge_vertices[v][vi][2] == -1 \
                            or vi < v and edge_vertices[vi][v][2] == -1:
                        adjacent_boundary_vertices.append(vi)

                # boundary case
                if len(adjacent_boundary_vertices) == 2:
                    value = [6 / 8 * vrtcs[v][idx] + 1 / 8 * sum(
                            vrtcs[k][idx] for k in adjacent_boundary_vertices)
                             for idx in dim_vertices_range]
                else:
                    beta = 1 / k * (
                            5 / 8 - (
                            3 / 8 + 1 / 4 * _np.cos(2 * _np.pi / k)) ** 2)
                    value = [(1 - k * beta) * vrtcs[v][idx] + beta * sum(
                            vrtcs[k][idx] for k in adjacent_vertices[v]) for idx
                             in dim_vertices_range]
                new_vertices[v] = value

            return [new_vertices[k] for k in
                    range(len(new_vertices))], new_faces

        def _add_edge_vertex(a, b, c, edge_vertices):
            # ensure right order of first two components
            if a > b:
                a, b = b, a

            # new vertex?
            if edge_vertices[a][b][0] == -1:
                edge_vertices[a][b][0] = _subdivide.index_vertex
                edge_vertices[a][b][1] = c
                # advance vertex index counter
                _subdivide.index_vertex += 1
            # existing vertex
            else:
                edge_vertices[a][b][2] = c

            # return values
            return edge_vertices[a][b][0]

        # initial corners and faces from the global constant
        vertices = Polyhedron.VERTICES_OCTAHEDRON
        faces = Polyhedron.FACES_OCTAHEDRON

        # initialize the subdivision algorithm
        _subdivide.index_vertex = len(vertices)

        # subdivide triangles into smaller ones using LOOP-SUBDIVISION
        # algorithm_old
        for level in range(depth):
            vertices, faces = _subdivide(vertices, faces)

        # convert into numpy arrays
        vertices = _np.asarray(vertices)
        faces = _np.asarray(faces)

        # normalise lengths of each corner to be unitary
        vertices /= _np.linalg.norm(vertices, axis=1)[:, _np.newaxis]

        # return a Polyhedron object with the corners shifted by the center
        # given through the user
        return Polyhedron(vertices + center[None, :], faces)

    @property
    def faces(self):
        return self._faces

    @property
    def surface(self):
        # just sum up over each tetrahedron's surface
        return _np.sum(self.surfaces, axis=0)

    @property
    def surfaces(self):
        # no cached result yet
        if self._surfaces is None:
            self._surfaces = self._calculate_surfaces()
        return self._surfaces

    @property
    def volume(self):
        # just sum up over each tetrahedron's volume
        return _np.sum(self.volumes, axis=0)

    @property
    def volumes(self):
        # no cached result yet
        if self._volumes is None:
            self._volumes = self._calculate_volumes()
        return self._volumes

    @property
    def vertices(self):
        return self._vertices

    def _calculate_centroid(self):
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

    def _calculate_surface(self):
        return _np.sum(self.surface, axis=0)

    def _calculate_surfaces(self):
        a = self.vertices[self.faces[:, 0], :]
        b = self.vertices[self.faces[:, 1], :]
        c = self.vertices[self.faces[:, 2], :]

        # heron's formula
        return 0.5 * _np.linalg.norm(_np.cross(a - b, a - c, axis=1), axis=1)

    def _calculate_volume(self):
        return _np.sum(self.volumes, axis=0)

    def _calculate_volumes(self):
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

    def __eq__(self, other):
        return super().__eq__(other) \
               and _np.allclose(self._vertices, other._vertices) \
               and _np.allclose(self._faces, other._faces)

    def __hash__(self):
        return hash((self.centroid, self.surface, self.volume,
                     self._vertices.shape[0], self._faces.shape[0]))

    __repr__ = make_repr(
            'centroid'
            'surface',
            'volume',
    )


__all__ = [
        'Polyhedron',
]
