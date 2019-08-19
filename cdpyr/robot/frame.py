from typing import Optional, Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.robot.anchor.frameanchor import (
    FrameAnchor,
    FrameAnchorList,
    FrameAnchorSchema,
)

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Frame(object):
    _anchors: FrameAnchorList

    def __init__(self,
                 anchors: Optional[
                     Union[FrameAnchorList, Sequence[FrameAnchor]]] = None
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


class FrameSchema(Schema):
    anchors = fields.List(fields.Nested(FrameAnchorSchema))

    __model__ = FrameAnchor

    @post_load
    def make_frame(self, data):
        return self.__model__(**data)


__all__ = ['Frame', 'FrameSchema']
