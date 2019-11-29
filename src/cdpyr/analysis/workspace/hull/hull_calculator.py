import itertools
from typing import (
    Sequence,
    Union,
)

import numpy as _np

from cdpyr.analysis.workspace import algorithm as _algorithm
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.hull import hull_result as _result
from cdpyr.robot import robot as _robot
from cdpyr.typing import (
    Matrix,
    Num,
    Vector,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class HullCalculator(_algorithm.Algorithm):
    _center: Vector
    depth: Num
    _faces: Matrix
    _index_vertex: int
    maximum_iterations: int
    maximum_halvings: int
    _vertices: Matrix

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 center: Union[Num, Vector] = None,
                 maximum_iterations: int = None,
                 maximum_halvings: int = None,
                 depth: int = None):
        super().__init__(archetype, criterion)
        self.center = center if center is not None else [0]
        self.maximum_iterations = maximum_iterations or 12
        self.maximum_halvings = maximum_halvings or 6
        self.depth = depth or 3
        self._index_vertex = None

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, center: Union[Num, Vector]):
        center = _np.asarray(center)

        if center.ndim == 0:
            center = _np.asarray([center])

        self._center = center

    @center.deleter
    def center(self):
        del self._center

    def _evaluate(self, robot: '_robot.Robot') -> '_result.Result':
        # a coordinate generator to get the grid of coordinates to evaluate
        search_directions, faces = self.__split_octahedron()

        # # termination conditions for each direction
        min_step = 0.5 ** self.maximum_halvings
        max_iters = self.maximum_iterations

        # calculate all vertices
        vertices = list(
            self.__check_direction(robot,
                                   direction,
                                   min_step,
                                   max_iters)
            for direction in search_directions)

        # return the hull result object
        return _result.HullResult(self,
                                  self._archetype,
                                  self._criterion,
                                  vertices,
                                  faces)

    def __check_direction(self, robot, direction: Vector, min_step, max_iters):
        # step length along this coordinate
        step_length = 1

        # iteration counter for reducing the likelihood to continue along
        # one search direction to infinity and beyond
        kiter = 0

        # init the current coordinate
        coordinate = self._center

        # as long as the step size isn't too small
        while step_length >= min_step and kiter <= max_iters:
            # calculate a trial coordinate along the search direction with
            # the current step length
            coordinate_trial = coordinate + step_length * direction

            # all poses are valid, so store the trial coordinate as
            # successful coordinate for the next loop
            if self._archetype.comparator(
                self._criterion.evaluate(robot, pose) for pose in
                self._archetype.poses(coordinate_trial)):
                # advance the pose
                coordinate = coordinate_trial
            # any pose is invalid at this coordinate, then we will reduce the
            # step size
            else:
                # halven step size
                step_length /= 2

            # increase iteration counter so that we don't continue along a
            # search direction too far
            kiter += 1

        # append the last coordinate as the vertex
        return coordinate

    def __split_octahedron(self):
        # original corners of an octahedron
        corners = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
        ]
        # original faces of an octahedron
        faces = [
            [0, 1, 2],
            [1, 3, 2],
            [3, 4, 2],
            [4, 0, 2],
            [0, 1, 5],
            [1, 3, 5],
            [3, 4, 5],
            [4, 0, 5],
        ]

        # subdivide triangles into smaller ones using LOOP-SUBDIVISION
        # algorithm_old
        for level in range(self.depth):
            corners, faces = self.__subdivide(corners, faces)

        # convert into numpy arrays
        corners = _np.asarray(corners)
        faces = _np.asarray(faces)

        # normalise lengths of each corner to be unitary
        corners /= _np.linalg.norm(corners, axis=1)[:, _np.newaxis]

        # and return the search directions as well as the faces
        return corners, faces

    def __subdivide(self, vertices: Sequence, faces: Sequence):
        new_faces = []
        num_vertices = len(vertices)
        dim_vertices = len(vertices[0])
        new_vertices = dict(zip(range(num_vertices), vertices))
        if self._index_vertex is None:
            self._index_vertex = num_vertices

        # matrix that holds which edges are adjacent to another
        edge_vertices = [
            [
                [
                    -1 for kx in range(dim_vertices)
                ]
                for ky in range(num_vertices)
            ]
            for kz in range(num_vertices)
        ]

        # create matrix of edge-vertices and new vertices
        for face in faces:
            a, b, c = face
            ab = self.__add_edge_vertex(a, b, c, edge_vertices)
            bc = self.__add_edge_vertex(b, c, a, edge_vertices)
            ac = self.__add_edge_vertex(a, c, b, edge_vertices)

            new_faces.extend([
                [a, ab, ac],
                [ab, b, bc],
                [ac, bc, c],
                [ac, ab, bc],
            ])

        # position of new vertices
        for v1, v2 in itertools.product(range(num_vertices),
                                        range(num_vertices)):
            vNIndex = edge_vertices[v1][v2][0]
            if vNIndex != -1:
                # catch boundary case
                if edge_vertices[v1][v2][2] == -1:
                    value = 1. / 2. * (vertices[v1][:] + vertices[v2][:])
                else:
                    value = [3 / 8 * (
                        vertices[v1][idx] + vertices[v2][idx]) + 1 / 8 * (
                                 vertices[edge_vertices[v1][v2][1]][idx] +
                                 vertices[edge_vertices[v1][v2][2]][idx])
                             for idx in range(dim_vertices)]

                new_vertices[vNIndex] = value

        # adjacent vertices
        adjacent_vertices = []
        for v, vTmp in itertools.product(range(num_vertices),
                                         range(num_vertices)):
            if v < vTmp and edge_vertices[v][vTmp][1] != -1 \
                or v > vTmp and edge_vertices[vTmp][v][1] != -1:
                try:
                    adjacent_vertices[v].append(vTmp)
                except IndexError as IndexE:
                    adjacent_vertices.insert(v, [vTmp])

        for v in range(num_vertices):
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
                value = [6 / 8 * vertices[v][idx] + 1 / 8 * _np.sum(
                    [vertices[k][idx] for k in adjacent_boundary_vertices],
                    axis=0)
                         for idx in range(dim_vertices)]
            else:
                beta = 1 / k * (
                    5 / 8 - (3 / 8 + 1 / 4 * _np.cos(2 * _np.pi / k)) ** 2)
                value = [(1 - k * beta) * vertices[v][idx] + beta * _np.sum(
                    [vertices[k][idx] for k in adjacent_vertices[v]], axis=0)
                         for
                         idx in range(dim_vertices)]
            new_vertices[v] = value

        return _np.asarray([new_vertices[k] for k in range(len(
            new_vertices))]), \
               new_faces

    def __add_edge_vertex(self, a, b, c, edge_vertices):
        # ensure right order of first two components
        if a > b:
            a, b = b, a

        # new vertex?
        if edge_vertices[a][b][0] == -1:
            edge_vertices[a][b][0] = self._index_vertex
            edge_vertices[a][b][1] = c
            # advance vertex index counter
            self._index_vertex += 1
        # existing vertex
        else:
            edge_vertices[a][b][2] = c

        # return values
        return edge_vertices[a][b][0]


__all__ = [
    'HullCalculator',
]
