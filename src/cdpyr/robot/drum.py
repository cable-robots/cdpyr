from typing import Optional

from magic_repr import make_repr

from cdpyr.geometry import primitive as _geometry
from cdpyr.mechanics import inertia as _inertia
from cdpyr.robot.robot_component import RobotComponent

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Drum(RobotComponent):
    geometry: '_geometry.Primitive'
    inertia: '_inertia.Inertia'

    def __init__(self,
                 geometry: Optional['_geometry.Primitive'] = None,
                 inertia: Optional['_inertia.Inertia'] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.geometry = geometry or _geometry.Primitive()
        self.inertia = inertia or _inertia.Inertia()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.geometry == other.geometry \
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
