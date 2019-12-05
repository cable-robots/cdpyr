from marshmallow import fields, post_load

from cdpyr.kinematics.transformation import angular as _angular
from cdpyr.schema.cdpyr_schema import CdpyrSchema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class AngularSchema(CdpyrSchema):
    dcm = fields.Tuple(
            (
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    ),
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    ),
                    fields.Tuple(
                            (fields.Float(), fields.Float(), fields.Float())
                    )
            ),
            missing=None
    )
    angular_velocity = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            missing=None,
            data_key='velocity'
    )
    angular_acceleration = fields.Tuple(
            (fields.Float(), fields.Float(), fields.Float()),
            missing=None,
            data_key='acceleration'
    )

    __model__ = _angular.Angular

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'AngularSchema',
]
