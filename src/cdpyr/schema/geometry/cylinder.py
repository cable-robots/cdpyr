from marshmallow import Schema, fields, post_load

from cdpyr.geometry import cylinder as _cylinder


class CylinderSchema(Schema):
    diameter = fields.Float()
    height = fields.Float()

    __model__ = _cylinder.Cylinder

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'CylinderSchema',
]
