from marshmallow import Schema, fields, post_load

from cdpyr.robot import pulley as _pulley
from cdpyr.schema.geometry import geometry as _geometry
from cdpyr.schema.kinematics.transformation import angular as _angular
from cdpyr.schema.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PulleySchema(Schema):
    geometry = fields.Nested(_geometry.GeometrySchema)
    inertia = fields.Nested(_inertia.InertiaSchema)
    angular = fields.Nested(_angular.AngularSchema)

    __model__ = _pulley.Pulley

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'PulleySchema',
]
