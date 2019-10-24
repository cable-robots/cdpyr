from marshmallow import Schema, fields, post_load

from cdpyr.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class InertiaSchema(Schema):
    angular = fields.List(fields.Float())
    linear = fields.List(fields.Float())

    __model__ = _inertia.Inertia

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'InertiaSchema'
]
