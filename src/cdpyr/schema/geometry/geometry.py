from marshmallow import Schema, fields, post_load

from cdpyr.geometry import geometry as _geometry

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GeometrySchema(Schema):
    mass = fields.Float()

    __model__ = _geometry.Geometry

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'GeometrySchema',
]
