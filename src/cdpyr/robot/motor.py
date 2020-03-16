from __future__ import annotations

from typing import AnyStr, Dict, Optional

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Motor(RobotComponent):
    inertia: Num
    rated_power: Num
    rated_speed: Num
    _torques: Dict[AnyStr, Num]

    def __init__(self,
                 torques: Optional[Dict[AnyStr, Num]] = None,
                 inertia: Optional[Num] = None,
                 rated_speed: Optional[Num] = None,
                 rated_power: Optional[Num] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.torques = {
                'stall': None,
                'peak':  None,
                'rated': None,
                'rms':   None
        }

        self.torques = torques or {}
        self.inertia = inertia or np_.inf
        self.rated_speed = rated_speed or np_.inf
        self.rated_power = rated_power or np_.inf

    @property
    def torques(self):
        return self._torques

    @torques.setter
    def torques(self, torques: Dict[AnyStr, Num]):
        self._torques = {
                **{'stall': None,
                   'peak':  None,
                   'rated': None,
                   'rms':   None},
                **torques}

    @torques.deleter
    def torques(self):
        del self._torques

    @property
    def stall_torque(self):
        return self.torques['stall']

    @stall_torque.setter
    def stall_torque(self, stall_torque: Num):
        self.torques['stall'] = stall_torque

    @stall_torque.deleter
    def stall_torque(self):
        del self.torques['stall']

    @property
    def peak_torque(self):
        return self.torques['peak']

    @peak_torque.setter
    def peak_torque(self, peak_torque: Num):
        self.torques['peak'] = peak_torque

    @peak_torque.deleter
    def peak_torque(self):
        del self.torques['peak']

    @property
    def rated_torque(self):
        return self.torques['rated']

    @rated_torque.setter
    def rated_torque(self, rated_torque: Num):
        self.torques['rated'] = rated_torque

    @rated_torque.deleter
    def rated_torque(self):
        del self.torques['rated']

    @property
    def rms_torque(self):
        return self.torques['rms']

    @rms_torque.setter
    def rms_torque(self, rms_torque: Num):
        self.torques['rms'] = rms_torque

    @rms_torque.deleter
    def rms_torque(self):
        del self.torques['rms']

    @property
    def max_torque(self):
        return self.peak_torque

    @max_torque.setter
    def max_torque(self, max_torque: Num):
        self.peak_torque = max_torque

    @max_torque.deleter
    def max_torque(self):
        del self.peak_torque

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.inertia == other.inertia \
               and self.rated_power == other.rated_power \
               and self.rated_speed == other.rated_power \
               and self.torques == other.torques

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.inertia,
                     self.rated_power,
                     self.rated_speed,
                     self.torques))

    __repr__ = make_repr(
            'torques',
            'rated_power',
            'rated_speed',
            'inertia'
    )


__all__ = [
        'Motor',
]
