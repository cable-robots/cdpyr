from __future__ import annotations

from typing import Optional

from magic_repr import make_repr

import numpy as np

from cdpyr.geometry import primitive as _geometry
from cdpyr.mechanics import inertia as _inertia
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Drum(RobotComponent):
    diameter: Num
    geometry: '_geometry.Primitive'
    inertia: '_inertia.Inertia'
    pitch: Num

    def __init__(self,
                 diameter: Optional[Num] = None,
                 pitch: Optional[Num] = None,
                 geometry: Optional['_geometry.Primitive'] = None,
                 inertia: Optional['_inertia.Inertia'] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.diameter = diameter or 0
        self.pitch = pitch or 0
        self.geometry = geometry or _geometry.Primitive()
        self.inertia = inertia or _inertia.Inertia()

    @property
    def radius(self):
        return self.diameter / 2

    @property
    def circumference(self):
        """
        Circumference of the drum calculated as :math:`2 \pi r`

        Returns
        -------
        u : Num
        """
        return 2 * np.pi * self.radius

    @property
    def length_per_turn(self):
        """
        Amount of cable that can be coiled in one turn

        Returns
        -------
        length : Num
        """

        return np.sqrt(self.circumference**2 + self.pitch**2)

    def num_windings(self, length: Num):
        """

        Calculate the number of windings for a given cable length
        Parameters
        ----------
        length : Num
            Length of cable to accommodate and calculate winding count for.

        Returns
        -------
        num : Num
            Number of windings as exact as possible
        """

        return length / self.length_per_turn

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.diameter == other.diameter \
               and self.pitch == other.pitch \
               and self.geometry == other.geometry \
               and self.inertia == other.inertia

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.geometry, self.inertia))

    __repr__ = make_repr(
            'geometry',
            'inertia'
    )


__all__ = [
        'Drum',
]
