from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.anchor.frameanchor import FrameAnchor
from cdpyr.robot.anchor.frameanchor import FrameAnchorList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Frame(object):
    _anchors: FrameAnchorList

    def __init__(self,
                 anchors: Optional[
                     Union[FrameAnchorList, Sequence[FrameAnchor]]] = None
                 ):
        self.anchors = anchors or []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: Union[FrameAnchorList, Sequence[FrameAnchor]]):
        if not isinstance(anchors, FrameAnchorList):
            anchors = FrameAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def ai(self):
        return np_.vstack(list(self.anchors.position))


Frame.__repr__ = make_repr(
    'anchors'
)

__all__ = ['Frame']
