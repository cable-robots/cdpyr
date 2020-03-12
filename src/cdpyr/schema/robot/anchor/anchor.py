from marshmallow import fields, post_load

from cdpyr.robot.anchor import anchor as _anchor
from cdpyr.schema.schema import Schema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class AnchorSchema(Schema):
    position = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            required=True,
    )
    dcm = fields.Tuple(
            (
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    ),
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    ),
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    )
            ),
            missing=None
    )

    __model__ = _anchor.Anchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _anchor.AnchorList(
                    (self.make_object(each, False, **kwargs) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'AnchorSchema',
]
