from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'GearboxSchema',
]

from marshmallow import fields, post_load

from cdpyr.robot import gearbox as _gearbox
from cdpyr.schema.schema import Schema


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
