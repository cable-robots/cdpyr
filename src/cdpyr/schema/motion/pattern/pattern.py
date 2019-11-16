from marshmallow import Schema, fields, post_load

from cdpyr.motion.pattern import pattern as _motion_pattern

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PatternSchema(Schema):
    dof_translation = fields.Int(data_key='translation')
    dof_rotation = fields.Int(data_key='rotation')

    __model__ = _motion_pattern.Pattern

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
    'PatternSchema',
]
