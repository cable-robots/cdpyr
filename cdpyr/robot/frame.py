from typing import Sequence
from typing import Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.anchor.frameanchor import FrameAnchor

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Frame(object):
    _anchors: Sequence[FrameAnchor]

    def __init__(self,
                 anchors: Sequence[FrameAnchor] = None
                 ):
        self.anchors = anchors if anchors is not None else []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: Sequence[FrameAnchor]):
        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def ai(self):
        def filter_(a: FrameAnchor):
            return a.position

        return map(filter_, self.anchors)


Frame.__repr__ = make_repr('anchors')

__all__ = ['Frame']
