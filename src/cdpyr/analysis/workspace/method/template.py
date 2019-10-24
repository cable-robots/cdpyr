from typing import Any, AnyStr, Dict, Sequence, Tuple

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import method as _method
from cdpyr.robot import robot as _robot


def evaluate(self: '_method.Method',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             archetype: '_archetype.Archetype',
             criterion: '_criterion.Criterion'):
    raise NotImplementedError


__vars__ = [
]
