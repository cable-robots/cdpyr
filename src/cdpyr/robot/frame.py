from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.anchor import frameanchor as _frameanchor


class Frame(object):
    _anchors: '_frameanchor.FrameAnchorList'

    def __init__(self,
                 anchors: Optional[
                     Union['_frameanchor.FrameAnchorList', Sequence[
                         '_frameanchor.FrameAnchor']]] = None
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
        '_frameanchor.FrameAnchorList', Sequence['_frameanchor.FrameAnchor']]):
        if not isinstance(anchors, _frameanchor.FrameAnchorList):
            anchors = _frameanchor.FrameAnchorList(anchors)

        self._anchors = anchors

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def ai(self):
        return np_.vstack(self.anchors.position).T


Frame.__repr__ = make_repr(
    'anchors'
)

__all__ = [
    'Frame',
]
