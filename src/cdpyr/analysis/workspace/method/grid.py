import itertools
from typing import Any, AnyStr, Dict, Sequence, Tuple, Union

import numpy as np_

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot
from cdpyr.typing import Num, Vector


def evaluate(self: '_method.Method',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             archetype: '_archetype.Archetype',
             criteria: Sequence[Tuple[
                 '_criterion.Criterion',
                 Dict[AnyStr, Any]
             ]]):
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
            value = [pose]
            # evaluate each criterion
            for criterion, _ in criteria:
                # append criterion and the flag of the criterion at the pose
                # to the list of values
                value.append((criterion, criterion.evaluate(robot, calculator, pose)))
            # append the evaluated criteria at the current pose
            flags.append(value)

        # append the current coordinate and the
        workspace.append(
            (coordinate, list(archetype.comparator(flag[1]) for flag in flags)))

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
        step = np_.repeat(step, np_.ceil(min_coord.size / step.size))[0:min_coord.size]

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

# from typing import Dict, Sequence, Tuple, AnyStr
#
# import numpy as np_
#
# from cdpyr.analysis.workspace.archetype import archetype as _archetype
# from cdpyr.analysis.workspace.method import method as _workspace
# from cdpyr.analysis.workspace.criterion import criterion as _criterion
# from cdpyr.motion.pose import generator as _generator, pose as _pose
# from cdpyr.robot import robot as _robot
#
#
# def evaluate(calculator: '_workspace.Calculator',
#              robot: '_robot.Robot',
#              archetype: '_archetype.Archetype',
#              criteria: Sequence[Tuple['_criterion.Criterion', Dict]],
#              **kwargs):
#     # get the start and end corner from the method
#     start = getcorner('start', calculator, robot)
#     end = getcorner('end', calculator, robot)
#
#     # a pose generator to get the grid of poses to evaluate
#     grid = _generator.steps(start, end, getattr(calculator, 'step', 10))
#
#     # list of coordinates that were evaluated
#     poses = []
#     flags = []
#
#     # we will start off of the pose generator we have created given the
#     # arguments
#     for coordinate in grid:  # THIS IS PART OF THE WORKSPACE ALGORITHM
#         # ask the archetype to validate the current coordinate on all criteria
#         checked_poses, checked_flags = archetype(robot,
#                                                  coordinate,
#                                                  criteria,
#                                                  **kwargs)
#
#         # append the result to the list of poses we checked
#         poses.append(checked_poses)
#         flags.append(checked_flags)
#
#     # return the tuple of poses that were evaluated
#     return poses, flags
#
#
# def defaults():
#     return {
#         'start': None,
#         'end':   None,
#         'step':  10,
#     }
#
#
# def getcorner(pos: AnyStr,
#               calculator: '_workspace.Calculator',
#               robot: '_robot.Robot'):
#     # get the attribute from the method first
#     pos = getattr(calculator, pos, [0.0, 0.0, 0.0])
#
#     # if start is empty, default to the lowest frame anchor
#     if pos is None:
#         if pos == 'end':
#             pos = np_.max(robot.ai, axis=1)
#         else:
#             pos = np_.min(robot.ai, axis=1)
#
#     # ensure we are returning a pose object from here
#     return pos if isinstance(pos, _pose.Pose) else _pose.Pose((pos,
#     np_.eye(3)))
