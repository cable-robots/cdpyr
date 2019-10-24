from marshmallow import Schema, fields, post_load

from cdpyr.geometry import tube as _tube

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class TubeSchema(Schema):
    inner_diameter = fields.Float()
    outer_diameter = fields.Float()
    height = fields.Float()

    __model__ = _tube.Tube

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'TubeSchema',
]
