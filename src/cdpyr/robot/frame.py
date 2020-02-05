from __future__ import annotations

from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.robot.anchor import frame_anchor as _frame_anchor
from cdpyr.robot.robot_component import RobotComponent

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Frame(RobotComponent):
    _anchors: _frame_anchor.FrameAnchorList

    def __init__(self,
                 anchors: Optional[
                     Union[_frame_anchor.FrameAnchorList, Sequence[
                         _frame_anchor.FrameAnchor]]] = None,
                 **kwargs):
        """ A general cable robot frame object.

        For the time being, this object only collects all frame anchors and
        provides a nice wrapper around accessing the anchor data.

        :param Union[FrameAnchorList, Sequence[FrameAnchor]] anchors:
        Optional list of anchors or a `FrameAnchorList` available on the frame.
        """
        super().__init__(**kwargs)
        self.anchors = anchors or []

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, anchors: Union[
        _frame_anchor.FrameAnchorList, Sequence[
            _frame_anchor.FrameAnchor]]):
        self._anchors = _frame_anchor.FrameAnchorList(anchors)

    @anchors.deleter
    def anchors(self):
        del self._anchors

    @property
    def num_anchors(self):
        return len(self._anchors)

    @property
    def ai(self):
        return np_.vstack([anchor.position for anchor in self.anchors]).T

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(
                this == that for this, that in zip(self.anchors, other.anchors))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.anchors)

    __repr__ = make_repr(
            'anchors'
    )


__all__ = [
        'Frame',
]
