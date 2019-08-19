from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Motor(object):
    _torques: dict
    _moment_of_inertia: _TNum
    _rated_speed: _TNum
    _rated_power: _TNum

    def __init__(self, torques: dict = None, inertia: _TNum = None,
                 rated_speed: _TNum = None, rated_power: _TNum = None):
        self.torques = {
            'stall': None,
            'peak':  None,
            'rated': None,
            'rms':   None
        }

        self.torques = torques or {}
        self.moment_of_inertia = inertia or 0
        self.rated_speed = rated_speed or None
        self.rated_power = rated_power or None

    @property
    def torques(self):
        return self._torques

    @torques.setter
    def torques(self, torques: dict):
        default = {'stall': None, 'peak': None, 'rated': None, 'rms': None}
        torques = torques or {}

        self._torques = {**default, **torques}

    @torques.deleter
    def torques(self):
        del self._torques

    @property
    def stall_torque(self):
        return self.torques['stall']

    @stall_torque.setter
    def stall_torque(self, stall_torque: _TNum):
        if stall_torque <= 0:
            raise ValueError('stall_torque must be positive')

        self.torques['stall'] = stall_torque

    @stall_torque.deleter
    def stall_torque(self):
        del self.torques['stall']

    @property
    def peak_torque(self):
        return self.torques['peak']

    @peak_torque.setter
    def peak_torque(self, peak_torque: _TNum):
        if peak_torque <= 0:
            raise ValueError('peak_torque must be positive')

        self.torques['peak'] = peak_torque

    @peak_torque.deleter
    def peak_torque(self):
        del self.torques['peak']

    @property
    def rated_speed(self):
        return self._rated_speed

    @rated_speed.setter
    def rated_speed(self, rated_speed: _TNum):
        if rated_speed <= 0:
            raise ValueError('rated_speed must be positive')

        self._rated_speed = rated_speed

    @rated_speed.deleter
    def rated_speed(self):
        del self._rated_speed

    @property
    def rated_power(self):
        return self._rated_power

    @rated_power.setter
    def rated_power(self, rated_power: _TNum):
        if rated_power <= 0:
            raise ValueError('rated_power must be positive')

        self._rated_power = rated_power

    @rated_power.deleter
    def rated_power(self):
        del self._rated_power

    @property
    def rated_torque(self):
        return self.torques['rated']

    @rated_torque.setter
    def rated_torque(self, rated_torque: _TNum):
        if rated_torque <= 0:
            raise ValueError('rated_torque must be positive')

        self.torques['rated'] = rated_torque

    @rated_torque.deleter
    def rated_torque(self):
        del self.torques['rated']

    @property
    def moment_of_inertia(self):
        return self._moment_of_inertia

    @moment_of_inertia.setter
    def moment_of_inertia(self, moment_of_inertia: _TNum):
        if moment_of_inertia < 0:
            raise ValueError('moment_of_inertia must be nonnegative')

        self._moment_of_inertia = moment_of_inertia

    @moment_of_inertia.deleter
    def moment_of_inertia(self):
        del self._moment_of_inertia

    @property
    def rms_torque(self):
        return self.torques['rms']

    @rms_torque.setter
    def rms_torque(self, rms_torque: _TNum):
        if rms_torque <= 0:
            raise ValueError('rms_torque must be positive')

        self.torques['rms'] = rms_torque

    @rms_torque.deleter
    def rms_torque(self):
        del self.torques['rms']

    @property
    def max_torque(self):
        return self.peak_torque

    @max_torque.setter
    def max_torque(self, max_torque: _TNum):
        if max_torque <= 0:
            raise ValueError('max_torque must be positive')

        self.peak_torque = max_torque

    @max_torque.deleter
    def max_torque(self):
        del self.peak_torque


Motor.__repr__ = make_repr(
    'torques',
    'rated_power',
    'rated_speed',
    'moment_of_inertia'
)

__all__ = ['Motor']
