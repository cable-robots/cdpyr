import numpy as _np
from marshmallow import fields, post_load

from cdpyr.robot import cable as _cable
from cdpyr.schema.schema import Schema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CableSchema(Schema):
    name = fields.String(
            missing=None
    )
    material = fields.String(
            missing=None
    )
    diameter = fields.Float(
            required=True
    )
    modulus = fields.Dict(
            keys=fields.String(),
            values=fields.List(
                    fields.Float(),
                    allow_none=True
            ),
            missing=None
    )
    color = fields.String(
            missing=None
    )
    breaking_load = fields.Float(
            missing=None,
            allow_nan=True
    )
    density = fields.Float(
            missing=_np.Infinity,
            allow_nan=True,
    )

    __model__ = _cable.Cable

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _cable.CableList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'CableSchema',
]
