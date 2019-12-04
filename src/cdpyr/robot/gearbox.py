from typing import Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Gearbox(RobotComponent):
    inertia: Num
    ratio: Num

    def __init__(self,
                 ratio: Optional[Num] = None,
                 inertia: Optional[Num] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.ratio = ratio or 1
        self.inertia = inertia or np_.Inf

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.inertia == other.inertia \
               and self.ratio == other.ratio

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.inertia, self.ratio))

    __repr__ = make_repr(
            'ratio',
            'inertia'
    )


__all__ = [
        'Gearbox',
]
