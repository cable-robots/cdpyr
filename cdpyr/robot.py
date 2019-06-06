import pathlib as pl_
from typing import List
from typing import Union

import numpy as np_

from cdpyr.components.anchor import Anchor
from cdpyr.components.cable import Cable
from cdpyr.components.connectivity import Connectivity
from cdpyr.components.platform import Platform


class Robot(object):
    _anchors: List[Anchor]
    _platforms: List[Platform]
    _cables: List[Cable]
    _connectivities: List[Connectivity]

    def __init__(self):
        pass

    @staticmethod
    def load(f: Union[str, pl_.Path]):
        pass

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: List[Anchor]):
        self._anchors = anchors

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self, platforms: List[Platform]):
        self._platforms = platforms

    @property
    def cables(self):
        return self._cables

    @cables.setter
    def cables(self, cables: List[Cable]):
        self._cables = cables

    @property
    def connectivities(self):
        return self._connectivities

    @connectivities.setter
    def connectivities(self, connectivities: List[Connectivity]):
        self._connectivities = connectivities

    @property
    def num_cables(self):
        return len(self.cables)

    @property
    def num_platforms(self):
        return len(self._platforms)

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def ai(self):
        return np_.stack([a.linear_position.T for a in self.anchors], axis=0)

    @property
    def bi(self):
        return np_.stack([p.bi for p in self.platforms], axis=2)

    @property
    def ri(self):
        return np_.stack([a.pulley.radius_outer for a in self.anchors], axis=0)
