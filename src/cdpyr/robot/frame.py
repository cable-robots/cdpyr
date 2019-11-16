from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject
from cdpyr.robot.anchor import frame_anchor as _frame_anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Frame(BaseObject):
    _anchors: '_frame_anchor.FrameAnchorList'

    def __init__(self,
                 anchors: Optional[
                     Union['_frame_anchor.FrameAnchorList', Sequence[
                         '_frame_anchor.FrameAnchor']]] = None
                 ):
        """ A general cable robot frame object.

        For the time being, this object only collects all frame anchors and
        provides a nice wrapper around accessing the anchor data.

        :param Union[FrameAnchorList, Sequence[FrameAnchor]] anchors:
        Optional list of anchors or a `FrameAnchorList` available on the frame.
        """
        self.anchors = anchors or []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: Union[
        '_frame_anchor.FrameAnchorList', Sequence[
            '_frame_anchor.FrameAnchor']]):
        if not isinstance(anchors, _frame_anchor.FrameAnchorList):
            anchors = _frame_anchor.FrameAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def ai(self):
        return np_.vstack([anchor.position for anchor in self.anchors]).T

    __repr__ = make_repr(
        'anchors'
    )


__all__ = [
    'Frame',
]
