from typing import Optional

from magic_repr import make_repr
from marshmallow import Schema, fields

from cdpyr.robot.drum import Drum
from cdpyr.robot.gearbox import Gearbox
from cdpyr.robot.motor import Motor, MotorSchema


class DriveTrain(object):
    _gearbox: Gearbox
    _drum: Drum
    _motor: Motor

    def __init__(self,
                 drum: Optional[Drum] = None,
                 motor: Optional[Motor] = None,
                 gearbox: Optional[Gearbox] = None
                 ):
        self.drum = drum or None
        self.motor = motor or None
        self.gearbox = gearbox or None

    @property
    def drum(self):
        return self._drum

    @drum.setter
    def drum(self, drum: Drum):
        self._drum = drum

    @drum.deleter
    def drum(self):
        del self._drum

    @property
    def gearbox(self):
        return self._gearbox

    @gearbox.setter
    def gearbox(self, gearbox: gearbox):
        self._gearbox = gearbox

    @gearbox.deleter
    def gearbox(self):
        del self._gearbox

    @property
    def motor(self):
        return self._motor

    @motor.setter
    def motor(self, motor: motor):
        self._motor = motor

    @motor.deleter
    def motor(self):
        del self._motor


DriveTrain.__repr__ = make_repr(
    'motor',
    'gearbox',
    'drum'
)


class DriveTrainSchema(Schema):
    motor = fields.Nested(MotorSchema)


__all__ = ['DriveTrain']
