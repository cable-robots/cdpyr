from enum import Enum

from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.analysis.workspace.method import crosssection, grid, hull
from cdpyr.robot import robot as _robot

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Method(Enum):
    CROSSSECTION = [crosssection]
    GRID = [grid]
    HULL = [hull]

    def __init__(self, *args):
        try:
            for name, value in args[0][0].__vars__:
                setattr(self, name, value() if callable(value) else value)
        except AttributeError as AttributeException:
            pass

    @property
    def implementation(self):
        return self._value_[0]

    def evaluate(self,
                 robot: '_robot.Robot',
                 calculator: '_calculator.Calculator',
                 archetype: '_archetype.Archetype',
                 criterion: '_criterion.Criterion'):
        return self.implementation.evaluate(self,
                                            robot,
                                            calculator,
                                            archetype,
                                            criterion)

    def __dir__(self):
        """
        We extend the list of properties of this object by the content of
        list `__vars__` of the underlying algorithm. Unfortunately, this only
        works when in the console and not in an IDE like PyCharm.

        Returns
        -------
        dir : list
        """
        keys = super(Enum, self).__dir__()
        try:
            keys = keys + list(var[0] for var in self.implementation.__vars__)
        except AttributeError as AttributeException:
            pass

        return keys
