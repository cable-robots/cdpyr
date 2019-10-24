import numpy as np_
from marshmallow import fields

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Numpy(fields.Field):

    def _serialize(self, value, attr, obj):
        if value is None:
            return ''

        return list(value)

    def _deserialize(self, value, attr, data):
        if value == '':
            return None

        if isinstance(value, list):
            return np_.asarray(value)

        return np_.asscalar(np_.asarray(value))


__all__ = [
    'Numpy'
]
