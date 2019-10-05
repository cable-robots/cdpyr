from typing import Optional

from magic_repr import make_repr

from cdpyr.robot import (
    drum as __drum,
    gearbox as __gearbox,
    motor as __motor,
)


class DriveTrain(object):
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


DriveTrain.__repr__ = make_repr(
    'motor',
    'gearbox',
    'drum'
)

__all__ = [
    'DriveTrain',
]
