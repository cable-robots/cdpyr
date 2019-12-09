from typing import Union

import numpy as _np

from cdpyr.analysis.workspace import workspace as _workspace
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.geometry import polyhedron as _polyhedron
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(_workspace.Algorithm):
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
                 depth: int = None,
                 **kwargs):
        super().__init__(archetype, criterion, **kwargs)
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

    def _evaluate(self, robot: '_robot.Robot') -> 'Result':
        # use our `Polyhedron` class and let it calculate the search
        # directions and faces
        polyhedron = _polyhedron.Polyhedron.from_octahedron(self.depth,
                                                            self.center)

        # a coordinate generator to get the coordinates to evaluate
        search_directions, faces = polyhedron.vertices, polyhedron.faces

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
        return Result(self,
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


class Result(_polyhedron.Polyhedron, _workspace.Result):

    def __init__(self,
                 algorithm: 'Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 vertices: Matrix,
                 faces: Matrix,
                 **kwargs):
        super().__init__(algorithm=algorithm, archetype=archetype,
                         criterion=criterion, vertices=vertices, faces=faces,
                         **kwargs)


__all__ = [
        'Algorithm',
        'Result',
]
