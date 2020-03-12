from marshmallow import fields, post_load

from cdpyr.robot import kinematicchain as _kinematicchain
from cdpyr.schema.schema import Schema

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicChainSchema(Schema):
    frame_anchor = fields.Integer(
            required=True
    )
    platform = fields.Integer(
            required=False,
            default=0,
            missing=0,
    )
    platform_anchor = fields.Integer(
            required=True
    )
    cable = fields.Integer(
            required=True
    )

    __model__ = _kinematicchain.KinematicChain

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _kinematicchain.KinematicChainList(
                    (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
        'KinematicChainSchema',
]
