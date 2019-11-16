from marshmallow import Schema, fields, post_load

from cdpyr.robot import gearbox as _gearbox

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GearboxSchema(Schema):
    ratio = fields.Float(
        missing=None
    )
    inertia = fields.Float(
        missing=None
    )

    __model__ = _gearbox.Gearbox

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'GearboxSchema',
]
