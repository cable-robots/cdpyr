from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot


def coordinates(method: '_method.Method',
                robot: '_robot.Robot'):
    raise NotImplementedError

# from typing import AnyStr, Dict, Sequence, Tuple
#
# import numpy as np_
#
# from cdpyr.analysis.workspace.archetype import archetype as _archetype
# from cdpyr.analysis.workspace.method import method as _workspace
# from cdpyr.analysis.workspace.criterion import criterion as _criterion
# from cdpyr.motion.pose import generator as _generator, pose as _pose
# from cdpyr.robot import robot as _robot
# from cdpyr.typing import Vector
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
#     # the search directions
#     search_directions = []
#
#     # list of coordinates that were evaluated
#     poses = []
#     flags = []
#
#     # we will start off of the pose generator we have created given the
#     # arguments
#     for search_direction in search_directions:  # THIS IS PART OF THE
#         pass
#         # # WORKSPACE ALGORITHM
#         # # ask the archetype to validate the current coordinate on all
#         criteria
#         # checked_poses, checked_flags = archetype(robot,
#         #                                          coordinate,
#         #                                          criteria,
#         #                                          **kwargs)
#
#         # # append the result to the list of poses we checked
#         # poses.append(checked_poses)
#         # flags.append(checked_flags)
#
#     # return the tuple of poses that were evaluated
#     return poses, flags
#
#
# def line_search(calculator: '_workspace.Calculator',
#                 robot: '_robot.Robot',
#                 archetype: '_archetype.Archetype',
#                 criteria: Sequence[Tuple['_criterion.Criterion', Dict]],
#                 center: Vector,
#                 line: Vector,
#                 epsilon: 1e-6,
#                 **kwargs):
#     # bounds of the line length
#     lower_bound = 0
#     upper_bound = 1
#
#     # sscaling factor of going along the line
#     scale = 1
#
#     # break criterion
#
#
#     # as long as we have not found the point where we break through the
#     # workspace hull
#     while abs(upper_bound - lower_bound) > epsilon:
#         scale = upper_bound - lower_bound
#         current_coordinate = center + scale * line
#
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
