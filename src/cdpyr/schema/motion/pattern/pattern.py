from marshmallow import fields, post_load

from cdpyr.motion import pattern as _pattern
from cdpyr.schema.schema import Schema

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

    __model__ = _pattern.Pattern

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(translation=data['dof_translation'],
                              rotation=data['dof_rotation'])


__all__ = [
        'PatternSchema',
]
