import itertools
from typing import Union

import numpy as np_

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def evaluate(self: '_method.Method',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             archetype: '_archetype.Archetype',
             criterion: '_criterion.Criterion'):
    # get min and maximum coordinates
    min_coord = np_.asarray(self.min)
    max_coord = np_.asarray(self.max)

    # a coordinate generator to get the grid of coordinates to evaluate
    grid = coordinates(min_coord, max_coord, self.step)

    # workspace list
    workspace = []

    # we will start off of the pose generator we have created given the
    # arguments
    for coordinate in grid:  # THIS IS PART OF THE WORKSPACE ALGORITHM
        # local values
        flags = []

        # loop over each pose the archetype provides at this coordinate
        for pose in archetype.poses(coordinate):
            flags.append(criterion.evaluate(robot, calculator, pose))

        workspace.append((coordinate, archetype.comparator(flags)))

    # return the tuple of poses that were evaluated
    return workspace


def coordinates(min_coord: Vector, max_coord: Vector, step: Union[Num, Vector]):
    # get an array
    step = np_.asarray(step)

    # convert scalar arrays into vectorial arrays
    if step.ndim == 0:
        step = np_.asarray([step])

    # make sure the number of steps is 6 i.e., one per spatial degree of freedom
    if step.size != min_coord.size:
        step = np_.repeat(step, np_.ceil(min_coord.size / step.size))[
               0:min_coord.size]

    # differences in position
    diff_pos = max_coord - min_coord

    # delta in position to perform per step
    deltas = diff_pos / step
    # set deltas to zero where no step is needed
    deltas[np_.isclose(step, 0)] = 0

    # how many iterations to perform per axis
    iterations = step * np_.logical_not(np_.isclose(diff_pos, 0))

    # TODO make creation of rotation matrix faster as `from_euler` seems to
    #  be a major bottleneck here
    # return the generator object
    return (min_coord + deltas * a for a in itertools.product(
        *(range(0, iterations[k] + 1) for k in range(0, len(iterations)))
    ))


__vars__ = [
    ('min', np_.zeros((3,))),
    ('max', np_.zeros((3,))),
    ('step', 5),
    ('UNIFORM', 'UNIFORM'),
    ('RANDOM', 'RANDOM'),
]
