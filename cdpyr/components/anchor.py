from typing import Iterable
from typing import List
from typing import Union

import numpy as np_
from scipy.spatial.transform import Rotation as Rotation_

from cdpyr.kinematics.transform import Angular
from cdpyr.kinematics.transform import Linear
from cdpyr.components.pulley import Pulley
from cdpyr.components.winch import Winch


class Anchor(Angular, Linear):

    _pulley: Pulley
    _winch: Winch

    def __init__(self, *args, **kwargs):
        Linear.__init__(self, *args, **kwargs)
        Angular.__init__(self, *args, **kwargs)

    @property
    def pulley(self):
        return self._pulley

    @pulley.setter
    def pulley(self, pulley: Pulley):
        self._pulley = pulley

    @property
    def winch(self):
        return self._winch

    @winch.setter
    def winch(self, winch: Winch):
        self._winch = winch
