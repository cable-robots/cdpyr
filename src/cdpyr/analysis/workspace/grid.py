import itertools
import multiprocessing
from collections import abc
from typing import Union

import numpy as _np
from joblib import Parallel, delayed
from scipy.spatial import Delaunay as _Delaunay

from cdpyr.analysis.workspace import workspace as _workspace
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.criterion import criterion as _criterion
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(_workspace.Algorithm):
    _lower_bound: Vector
    _upper_bound: Vector
    _steps: Vector

    def __init__(self,
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 lower_bound: Union[Num, Vector] = None,
                 upper_bound: Union[Num, Vector] = None,
                 steps: Union[Num, Vector] = None,
                 **kwargs):
        super().__init__(archetype, criterion, **kwargs)
        self.lower_bound = lower_bound if lower_bound is not None else [0]
        self.upper_bound = upper_bound if upper_bound is not None else [0]
        self.steps = steps if steps is not None else [1]

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, bound: Union[Num, Vector]):
        bound = _np.asarray(bound)
        if bound.ndim == 0:
            bound = _np.asarray([bound])

        self._lower_bound = bound

    @lower_bound.deleter
    def lower_bound(self):
        del self._lower_bound

    @property
    def upper_bound(self):
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, bound: Union[Num, Vector]):
        bound = _np.asarray(bound)
        if bound.ndim == 0:
            bound = _np.asarray([bound])

        self._upper_bound = bound

    @upper_bound.deleter
    def upper_bound(self):
        del self._upper_bound

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps: Union[Num, Vector]):
        steps = _np.asarray(steps)
        if steps.ndim == 0:
            steps = _np.asarray([steps])

        if steps.size != self._lower_bound.size:
            steps = _np.repeat(steps,
                               self._lower_bound.size - (steps.size - 1))[
                    0:self._lower_bound.size]

        self._steps = steps

    def coordinates(self):
        # differences in position
        diff_pos = self._upper_bound - self._lower_bound

        # delta in position to perform per step
        deltas = diff_pos / self._steps
        # set deltas to zero where no step is needed
        deltas[_np.isclose(self._steps, 0)] = 0

        # how many iterations to perform per axis
        iterations = self._steps * _np.logical_not(_np.isclose(diff_pos, 0))

        # return a generator object of coordinates
        return (self._lower_bound + deltas * a for a in itertools.product(
                *(range(0, iterations[k] + 1) for k in
                  range(0, len(iterations)))
        ))

    def _evaluate(self, robot: '_robot.Robot', *args, **kwargs) -> 'Result':
        # parallelized evaluation
        if kwargs.pop('parallel', False):
            n_jobs = kwargs.pop('n_jobs', multiprocessing.cpu_count())
            coordinates, flags = zip(
                *Parallel(n_jobs=n_jobs, **kwargs)(
                        delayed(self.__check__coordinate)(robot, coordinate) for
                        coordinate in self.coordinates()))
        # non-parallelized, fancy list comprehension
        else:
            coordinates, flags = list(zip(
                *((coordinate, self.__check__coordinate(robot, coordinate)) for
                  coordinate in self.coordinates())))

        # return the tuple of poses that were evaluated
        return Result(
                self,
                self._archetype,
                self._criterion,
                coordinates,
                flags
        )

    def __check__coordinate(self, robot, coordinate: _np.ndarray):
        # we don't want to loose too much type looking up variables inside
        # this object, so we will store them as local variables here
        criterion_evaluator = self._criterion.evaluate
        poses = self._archetype.poses

        # and compare
        return coordinate, self._archetype.comparator(
                criterion_evaluator(robot, pose)
                for pose in poses(coordinate))


class Result(_workspace.Result, abc.Collection):
    _coordinates: Matrix
    _flags: Vector
    _inside: Matrix
    _outside: Matrix

    def __init__(self,
                 algorithm: 'Algorithm',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion',
                 coordinates: Matrix,
                 flags: Vector,
                 **kwargs):
        super().__init__(algorithm, archetype, criterion, **kwargs)
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

    @property
    def surface_area(self):
        if self._surface is None:
            try:
                # triangulate all points that are inside the workspace
                delau = _Delaunay(self.inside)
                # convex null of this area will be used to determine the
                # workspace volume and surface area
                hull_faces = delau.convex_hull
                # get each vertex
                f0 = self.inside[hull_faces[:, 0], :]
                f1 = self.inside[hull_faces[:, 1], :]
                f2 = self.inside[hull_faces[:, 2], :]

                # length of each side
                a = _np.linalg.norm(f0 - f1, axis=1)
                b = _np.linalg.norm(f1 - f2, axis=1)
                c = _np.linalg.norm(f2 - f0, axis=1)

                # heron's formula
                self._surface = _np.sum(1.0 / 4.0 * _np.sqrt(
                        (a ** 2 + b ** 2 + c ** 2) ** 2 - 2 * (
                                a ** 4 + b ** 4 + c ** 4)), axis=0)
            except (IndexError, ValueError) as Error:
                self._surface = 0

        return self._surface

    @property
    def volume(self):
        if self._volume is None:
            try:
                delau = _Delaunay(self.inside)
                # convex null of this area will be used to determine the
                # workspace volume and surface area
                hull_faces = delau.convex_hull
                # get each vertex
                a = self.inside[hull_faces[:, 0], :]
                b = self.inside[hull_faces[:, 1], :]
                c = self.inside[hull_faces[:, 2], :]
                d = _np.zeros((3,))

                # | (a - d) . ( (b - d) x (c - d) ) |
                # -----------------------------------
                #                  6
                self._volume = _np.sum(_np.abs(
                        _np.sum((a - d) * _np.cross(b - d, c - d, axis=1),
                                axis=1))) / 6
            except (IndexError, ValueError) as Error:
                self._volume = 0

        return self._volume

    def __iter__(self):
        return ((self._coordinates[idx, :], self._flags[idx]) for idx in
                range(len(self)))

    def __getitem__(self, idx: int):
        return self._coordinates[idx, :], self._flags[idx]

    def __len__(self) -> int:
        try:
            return self._coordinates.shape[0]
        except AttributeError as AttributeE:
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
        except KeyError as KeyE:
            return False


__all__ = [
        'Algorithm',
        'Result',
]
