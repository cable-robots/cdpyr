from marshmallow import fields, post_load

from cdpyr.robot import frame as _frame
from cdpyr.schema.schema import Schema
from cdpyr.schema.robot.anchor import frame_anchor as _frame_anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameSchema(Schema):
    anchors = fields.Nested(
            _frame_anchor.FrameAnchorSchema(
                    many=True
            ),
            required=True,
    )

    __model__ = _frame.Frame

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'FrameSchema',
]
