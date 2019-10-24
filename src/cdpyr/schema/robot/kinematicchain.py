from marshmallow import Schema, fields, post_load

from cdpyr.robot import kinematicchain as _kinematicchain

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicChainSchema(Schema):
    frame_anchor = fields.Number()
    platform = fields.Number()
    platform_anchor = fields.Number()
    cable = fields.Number()

    __model__ = _kinematicchain.KinematicChain

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class KinematicChainListSchema(Schema):
    data = fields.List(fields.Nested(KinematicChainSchema))

    __model__ = _kinematicchain.KinematicChainList

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'KinematicChainSchema',
    'KinematicChainListSchema',
]
