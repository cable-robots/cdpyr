from typing import Optional

from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject
from cdpyr.robot import (
    drum as __drum,
    gearbox as __gearbox,
    motor as __motor,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DriveTrain(BaseObject):
    _gearbox: '__gearbox.Gearbox'
    _drum: '__drum.Drum'
    _motor: '__motor.Motor'

    def __init__(self,
                 drum: Optional['__drum.Drum'] = None,
                 motor: Optional['__motor.Motor'] = None,
                 gearbox: Optional['__gearbox.Gearbox'] = None
                 ):
        self.drum = drum or None
        self.motor = motor or None
        self.gearbox = gearbox or None

    @property
    def drum(self):
        return self._drum

    @drum.setter
    def drum(self, drum: '__drum.Drum'):
        self._drum = drum

    @drum.deleter
    def drum(self):
        del self._drum

    @property
    def gearbox(self):
        return self._gearbox

    @gearbox.setter
    def gearbox(self, gearbox: '__gearbox.Gearbox'):
        self._gearbox = gearbox

    @gearbox.deleter
    def gearbox(self):
        del self._gearbox

    @property
    def motor(self):
        return self._motor

    @motor.setter
    def motor(self, motor: '__motor.Motor'):
        self._motor = motor

    @motor.deleter
    def motor(self):
        del self._motor

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.drum == other.drum \
               and self.gearbox == other.gearbox \
               and self.motor == other.motor

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.drum, self.gearbox, self.motor))

    __repr__ = make_repr(
        'motor',
        'gearbox',
        'drum'
    )


__all__ = [
    'DriveTrain',
]
