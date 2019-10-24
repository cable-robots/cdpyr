from marshmallow import Schema, fields, post_load

from cdpyr.geometry import sphere as _sphere

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class SphereSchema(Schema):
    diameter = fields.Float()

    __model__ = _sphere.Sphere

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'SphereSchema',
]
