from typing import Iterable
from typing import List
from typing import Union

import numpy as np_
from scipy.spatial.transform import Rotation as Rotation_

from cdpyr.components.geometric import Cylinder
from cdpyr.kinematics.transform import Angular


class Pulley(Angular, Cylinder):

    def __init__(self, *args, **kwargs):
        Cylinder.__init__(self, *args, **kwargs)
        Angular.__init__(self, *args, **kwargs)
