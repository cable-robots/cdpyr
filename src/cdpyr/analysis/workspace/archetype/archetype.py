from typing import Callable

import numpy as np_
from enum import Enum

from cdpyr.analysis.workspace.archetype import (
    dextrous,
    inclusion_orientation,
    maximum,
    orientation,
    total_orientation,
    translation,
)


class Archetype(Enum):
    DEXTROUS = [dextrous]
    INCLUSION_ORIENTATION = [inclusion_orientation]
    MAXIMUM = [maximum]
    ORIENTATION = [orientation]
    TOTAL_ORIENTATION = [total_orientation]
    TRANSLATION = [translation]

    def __init__(self, *args):
        try:
            for name, value in args[0][0].__vars__:
                setattr(self, name, value() if callable(value) else value)
        except AttributeError as AttributeException:
            pass

    @property
    def implementation(self):
        return self._value_[0]

    @property
    def comparator(self) -> Callable:
        return self.implementation.comparator

    def poses(self, coordinate):
        """
        Determine all poses that should be checked for at the current
        coordinate of the workspace method algorithm.
        More precisely:
        TRANSLATION returns only a single pose at the current coordinate with
        the fixed rotation.
        ORIENTATION returns a list of poses with the orientations spanning in
        all of SO3.
        INCLUSION_ORIENTATION returns a list of poses with the orientations
        spanning in a set of orientations.
        MAXIMUM returns a list of poses with the orientations spanning in all
        of SO3.
        TOTAL_ORIENTATION returns a list of poses with the orientations
        spanning in a set of orientations.
        DEXTROUS returns a list of poses with the orientation spanning in all
        of SO3.


        Parameters
        ----------
        coordinate

        Returns
        -------

        """
        return self.implementation.poses(self, np_.pad(coordinate, (
        0, 3 - coordinate.size)))

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
            keys = keys + self.implementation.__vars__
        except AttributeError as AttributeException:
            pass

        return keys
