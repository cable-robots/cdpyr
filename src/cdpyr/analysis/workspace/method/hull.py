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
    raise NotImplementedError


__vars__ = [
    ('center', np_.zeros((3, ))),
    ('depth', 3)
]
