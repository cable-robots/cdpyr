from marshmallow import Schema, fields, post_load

from cdpyr.motion.pattern import pattern as _motion_pattern

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PatternSchema(Schema):
    dof_translation = fields.Int(
            required=True,
            data_key='translation',
            default=0
    )
    dof_rotation = fields.Int(
            required=True,
            data_key='rotation',
            default=0
    )

    __model__ = _motion_pattern.Pattern

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(translation=data['dof_translation'],
                              rotation=data['dof_rotation'])


__all__ = [
        'PatternSchema',
]
