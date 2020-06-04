from __future__ import annotations

from typing import Optional

from magic_repr import make_repr

from cdpyr.robot import drum as _drum, gearbox as _gearbox, motor as _motor
from cdpyr.robot.robot_component import RobotComponent

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Drivetrain(RobotComponent):
    gearbox: _gearbox.Gearbox
    drum: _drum.Drum
    motor: _motor.Motor

    def __init__(self,
                 drum: Optional[_drum.Drum] = None,
                 motor: Optional[_motor.Motor] = None,
                 gearbox: Optional[_gearbox.Gearbox] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.drum = drum or None
        self.motor = motor or None
        self.gearbox = gearbox or None

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
        'Drivetrain',
]
