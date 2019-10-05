from marshmallow import Schema, fields, post_load

from cdpyr.robot import cable as _cable


class CableSchema(Schema):
    name = fields.String()
    material = fields.String()
    diameter = fields.Float(required=True)
    modulus = fields.Dict(required=True)
    color = fields.String()
    breaking_load = fields.Float(required=True)

    __model__ = _cable.Cable

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class CableListSchema(Schema):
    data = fields.List(fields.Nested(CableSchema))

    __model__ = _cable.CableList

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'CableSchema',
    'CableListSchema',
]
