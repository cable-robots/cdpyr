from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Numpy',
]

import numpy as np_

from marshmallow import fields


class Numpy(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        elif value is np_.nan:
            return 'nan'

        try:
            return value.tolist()
        except AttributeError:
            return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value == '':
            return None
        elif value == 'nan':
            return np_.nan

        if isinstance(value, list):
            return np_.asarray(value)

        return np_.asscalar(np_.asarray(value))
