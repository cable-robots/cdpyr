from marshmallow import Schema, fields, post_load

from cdpyr.geometry import cuboid as _cuboid

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CuboidSchema(Schema):
    width = fields.Float()
    depth = fields.Float()
    height = fields.Float()

    __model__ = _cuboid.Cuboid

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'CuboidSchema',
]
