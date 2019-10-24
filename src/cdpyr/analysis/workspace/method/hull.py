import itertools

import numpy as np_

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def evaluate(self: '_method.Method',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             archetype: '_archetype.Archetype',
             criterion: '_criterion.Criterion'):
    try:
        center = np_.asarray(self.center)
    except AttributeError as AttributeException:
        center = np_.asarray([0.0, 0.0, 0.0])

    # a coordinate generator to get the grid of coordinates to evaluate
    search_directions, faces = split_octahedron(self.depth)

    # termination conditions for each direction
    min_step = 0.5 ** 6  # maximum halvings allowed
    max_iters = 12

    # stores workspace boundaries
    workspace = []

    # loop over each search direction
    for search_direction in search_directions:
        # step length along this coordinate
        step_length = 1

        # iteration counter for reducing the likelihood to continue along one
        # search direction to infinity and beyond
        kiter = 0

        # init the current coordinate
        coordinate = center

        # as long as the step size isn't too small
        while step_length >= min_step and kiter <= max_iters:
            # calculate a trial coordinate along the search direction with
            # the current step length
            coordinate_trial = coordinate + step_length * search_direction

            # flags of each criterion evaluated at the current coordinate
            flags = []

            # loop over each pose the archetype provides at this coordinate
            for pose in archetype.poses(coordinate_trial):
                flags.append(criterion.evaluate(robot, calculator, pose))

            # check if any pose is invalid at this coordinate, then we will
            # reduce the step size
            if not all(flags):
                # halven step size
                step_length /= 2
            # all poses are valid, so store the trial coordinate as
            # successful coordinate for the next loop
            else:
                # advance the pose
                coordinate = coordinate_trial

            # increase iteration counter so that we don't continue along a
            # search direction too far
            kiter += 1

        # append the current coordinate and the
        workspace.append((coordinate, archetype.comparator(flags)))

    return workspace, faces


def split_octahedron(depth: Num):
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

    # subdivide triangles into smaller ones using LOOP-SUBDIVISION algorithm
    for level in range(depth):
        corners, faces = subdivide(corners, faces)

    # convert into numpy arrays
    corners = np_.asarray(corners)
    faces = np_.asarray(faces)

    # normalise lengths of each corner to be unitary
    corners /= np_.linalg.norm(corners, axis=1)[:, np_.newaxis]

    # and return the search directions as well as the faces
    return corners, faces


def subdivide(vertices: Matrix, faces: Matrix):
    vertices: list
    faces: list

    new_faces = []
    num_vertices = len(vertices)
    dim_vertices = len(vertices[0])
    new_vertices = dict(zip(range(num_vertices), vertices))
    index_vertex = num_vertices

    # matrix that holds which edges are adjacent to another
    edge_vertices = [
        [[-1 for kx in range(dim_vertices)] for ky in range(num_vertices)] for
        kz in range(num_vertices)]

    # create matrix of edge-vertices and new vertices
    for face in faces:
        a, b, c = face
        ab, index_vertex = add_edge_vertex(a, b, c, edge_vertices, index_vertex)
        bc, index_vertex = add_edge_vertex(b, c, a, edge_vertices, index_vertex)
        ac, index_vertex = add_edge_vertex(a, c, b, edge_vertices, index_vertex)

        new_faces.extend([
            [a, ab, ac],
            [ab, b, bc],
            [ac, bc, c],
            [ac, ab, bc],
        ])

    # position of new vertices
    for v1, v2 in itertools.product(range(num_vertices), range(num_vertices)):
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
    for v, vTmp in itertools.product(range(num_vertices), range(num_vertices)):
        if v < vTmp and edge_vertices[v][vTmp][1] != -1 \
            or v > vTmp and edge_vertices[vTmp][v][1] != -1:
            try:
                adjacent_vertices[v].append(vTmp)
            except IndexError as IndexException:
                adjacent_vertices.insert(v, [vTmp])

    for v in range(num_vertices):
        try:
            k = len(adjacent_vertices[v])
        except IndexError as IndexException:
            continue

        adjacent_boundary_vertices = []
        for i in range(k):
            vi = adjacent_vertices[v][i]
            if vi > v and edge_vertices[v][vi][2] == -1 \
                or vi < v and edge_vertices[vi][v][2] == -1:
                adjacent_boundary_vertices.append(vi)

        # boundary case
        if len(adjacent_boundary_vertices) == 2:
            value = [6 / 8 * vertices[v][idx] + 1 / 8 * np_.sum(
                [vertices[k][idx] for k in adjacent_boundary_vertices], axis=0)
                     for idx in range(dim_vertices)]
        else:
            beta = 1 / k * (
                5 / 8 - (3 / 8 + 1 / 4 * np_.cos(2 * np_.pi / k)) ** 2)
            value = [(1 - k * beta) * vertices[v][idx] + beta * np_.sum(
                [vertices[k][idx] for k in adjacent_vertices[v]], axis=0) for
                     idx in range(dim_vertices)]
        new_vertices[v] = value

    return np_.asarray([new_vertices[k] for k in range(len(new_vertices))]), \
           new_faces


def add_edge_vertex(a, b, c, edge_vertices, index_vertex):
    # ensure right order of first two components
    if a > b:
        a, b = b, a

    # new vertex?
    if edge_vertices[a][b][0] == -1:
        edge_vertices[a][b][0] = index_vertex
        edge_vertices[a][b][1] = c
        # advance vertex index counter
        index_vertex += 1
    # existing vertex
    else:
        edge_vertices[a][b][2] = c

    # return values
    return edge_vertices[a][b][0], index_vertex


__vars__ = [
    ('center', np_.zeros((3,))),
    ('depth', 3)
]
