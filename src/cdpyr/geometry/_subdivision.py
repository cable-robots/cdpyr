from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

import functools
import itertools

import numpy as _np

from cdpyr.typing import Faces, Vertices


@functools.lru_cache(128)
def subdivide(vertices: Vertices, faces: Faces):
    dim_vertices = len(vertices[0])
    num_vertices = len(vertices)

    subdivide.index_vertex = num_vertices

    edge_vertices = [
            [
                    [-1 for kx in range(dim_vertices)]
                    for ky in range(num_vertices)
            ] for kz in range(num_vertices)
    ]

    new_faces = split_faces(faces, edge_vertices)
    new_vertices = _new_vertices(vertices, edge_vertices)
    adjacent_vertices = find_adjacent_vertices(vertices, edge_vertices)
    new_vertices = correct_vertices(vertices, new_vertices, adjacent_vertices,
                                    edge_vertices)

    subdivide.index_vertex = None

    return tuple(tuple(new_vertices[k]) for k in range(len(new_vertices))), \
           tuple(tuple(face) for face in new_faces)


def add_edge_vertex(a: int, b: int, c: int, edge_vertices):
    # ensure right order of first two components
    if a > b:
        a, b = b, a

    # new vertex?
    if edge_vertices[a][b][0] == -1:
        edge_vertices[a][b][0] = subdivide.index_vertex
        edge_vertices[a][b][1] = c
        # advance vertex index counter
        subdivide.index_vertex += 1
    # existing vertex
    else:
        edge_vertices[a][b][2] = c

    # return values
    return edge_vertices[a][b][0]


def split_faces(faces, edge_vertices):
    new_faces = []
    # create matrix of edge-vertices and new vertices
    for face in faces:
        a, b, c = face
        ab = add_edge_vertex(a, b, c, edge_vertices)
        bc = add_edge_vertex(b, c, a, edge_vertices)
        ac = add_edge_vertex(a, c, b, edge_vertices)

        new_faces.extend([
                [a, ab, ac],
                [ab, b, bc],
                [ac, bc, c],
                [ac, ab, bc],
        ])

    return new_faces


def _new_vertices(vertices, edge_vertices):
    num_vertices = len(vertices)
    dim_vertices = len(vertices[0])
    new_vertices = dict(zip(range(num_vertices), vertices))

    for v1, v2 in itertools.product(range(num_vertices), range(num_vertices)):
        vNIndex = edge_vertices[v1][v2][0]
        if vNIndex != -1:
            # catch boundary case
            if edge_vertices[v1][v2][2] == -1:
                value = 1. / 2. * (vertices[v1][:] + vertices[v2][:])
            else:
                value = [3 / 8 * (
                        vertices[v1][dim] + vertices[v2][dim]) + 1 / 8 * (
                                 vertices[edge_vertices[v1][v2][1]][dim] +
                                 vertices[edge_vertices[v1][v2][2]][dim])
                         for dim in range(dim_vertices)]

            new_vertices[vNIndex] = value

    return new_vertices


def find_adjacent_vertices(vertices, edge_vertices):
    num_vertices = len(vertices)

    adjacent_vertices = []

    for v, vTmp in itertools.product(range(num_vertices), range(num_vertices)):
        if v < vTmp and edge_vertices[v][vTmp][1] != -1 \
                or v > vTmp and edge_vertices[vTmp][v][1] != -1:
            try:
                adjacent_vertices[v].append(vTmp)
            except IndexError as IndexE:
                adjacent_vertices.insert(v, [vTmp])

    return adjacent_vertices


def correct_vertices(vertices, new_vertices, adjacent_vertices, edge_vertices):
    num_vertices = len(vertices)
    dim_vertices = len(vertices[0])

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
            value = [6 / 8 * vertices[v][dim] + 1 / 8 * sum(
                    vertices[k][dim] for k in adjacent_boundary_vertices)
                     for dim in range(dim_vertices)]
        else:
            beta = 1 / k * (
                    5 / 8 - (3 / 8 + 1 / 4 * _np.cos(2 * _np.pi / k)) ** 2)
            value = [(1 - k * beta) * vertices[v][dim] + beta * sum(
                    vertices[k][dim] for k in adjacent_vertices[v])
                     for dim in range(dim_vertices)]
        new_vertices[v] = value

    return new_vertices
