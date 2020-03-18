from __future__ import annotations

import multiprocessing
from typing import Union

import numpy as _np
from joblib import delayed, Parallel

from cdpyr.analysis.archetype import archetype as _archetype
from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.analysis.workspace import workspace as _workspace
from cdpyr.exceptions import InvalidPoseException
from cdpyr.geometry import polyhedron as _polyhedron
from cdpyr.motion import pose as _pose
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
                 archetype: _archetype.Archetype,
                 criterion: _criterion.Criterion,
                 center: Union[Num, Vector] = None,
                 maximum_iterations: int = None,
                 maximum_halvings: int = None,
                 depth: int = None,
                 **kwargs):
        super().__init__(archetype=archetype,
                         criterion=criterion,
                         **kwargs)
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

    def _evaluate(self, robot: _robot.Robot, *args, **kwargs) -> 'Result':
        # use our `Polyhedron` class and let it calculate the search
        # directions and faces
        polyhedron = _polyhedron.Polyhedron.from_octahedron(self.depth,
                                                            self.center)

        # a coordinate generator to get the coordinates to evaluate
        search_directions, faces = polyhedron.vertices, polyhedron.faces

        # # termination conditions for each direction
        min_step = 0.5 ** self.maximum_halvings
        max_iters = self.maximum_iterations

        # parallelized code of hull method
        if kwargs.pop('parallel', False):
            n_jobs = kwargs.pop('n_jobs', multiprocessing.cpu_count())
            vertices = Parallel(n_jobs=n_jobs, **kwargs)(
                    delayed(self.__check_direction)(robot, direction, min_step,
                                                    max_iters) for direction in
                    search_directions)
        # non-parallelized, list-comprehension code of hull method
        else:
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

        # quicker look ups
        archetype_ = self._archetype
        comparator_ = self._archetype.comparator
        criterion_ = self._criterion.evaluate

        # as long as the step size isn't too small
        while step_length >= min_step and kiter <= max_iters:
            # calculate a trial coordinate along the search direction with
            # the current step length
            coordinate_trial = coordinate + step_length * direction

            try:
                # evaluate criterion for every pose and compare the results
                # to be true according to the archetype
                if comparator_(criterion_(robot, pose)
                               for pose in archetype_.poses(coordinate_trial)):
                    coordinate = coordinate_trial
                # the archetype has not be validating all poses successfully,
                # so reduce step size
                else:
                    step_length /= 2
            # failure to determine a valid pose due to e.g., invalid force
            # distribution, so we will reduce the step size
            except InvalidPoseException:
                step_length /= 2
            # increase iteration counter so that we don't continue along a
            # search direction too far
            finally:
                kiter += 1

        # append the last coordinate as the vertex
        return coordinate


class Result(_polyhedron.Polyhedron, _workspace.Result):

    def __init__(self,
                 algorithm: Algorithm,
                 archetype: _archetype.Archetype,
                 criterion: _criterion.Criterion,
                 vertices: Matrix,
                 faces: Matrix,
                 **kwargs):
        _polyhedron.Polyhedron.__init__(self,
                                        vertices=vertices, faces=faces)
        _workspace.Result.__init__(self,
                                   algorithm=algorithm,
                                   archetype=archetype,
                                   criterion=criterion)

    def to_poselist(self):
        return _pose.PoseList((p
                               for c in self._vertices
                               for p in self._archetype.poses(c)))


__all__ = [
        'Algorithm',
        'Result',
]
