from typing import List
import numpy as np_

from cdpyr.components import Anchor
from cdpyr.components.geometric import Cube
from cdpyr.motionpattern import MotionPattern


class Platform(Cube):
    _anchors: List[Anchor]

    def __init__(self, anchors: List[Anchor] = None, *args, **kwargs):
        Cube.__init__(*args, **kwargs)
        self.anchors = anchors if anchors is not None else []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: List[Anchor]):
        self._anchors = anchors

    @property
    def bi(self):
        return np_.hstack([b.linear_position.T for b in self.anchors])
