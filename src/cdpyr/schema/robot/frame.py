from marshmallow import Schema, fields, post_load

from cdpyr.robot import frame as _frame
from cdpyr.schema.robot.anchor import frameanchor as _frame_anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameSchema(Schema):
    anchors = fields.List(fields.Nested(_frame_anchor.FrameAnchorSchema))

    __model__ = _frame.Frame

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'FrameSchema',
]
