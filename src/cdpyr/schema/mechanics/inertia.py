import numpy as np
from marshmallow import Schema, fields, post_load

from cdpyr.mechanics import inertia as _inertia

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class InertiaSchema(Schema):
    angular = fields.Tuple(
            (
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    )),
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    )),
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    ))
            ),
            required=False,
            default=[[np.inf, 0, 0], [0, np.inf, 0], [0, 0, np.inf]],
            missing=None
    )
    linear = fields.Tuple(
            (
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    )),
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    )),
                    fields.Tuple((
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True),
                            fields.Float(allow_nan=True)
                    ))
            ),
            required=False,
            default=[[np.inf, 0, 0], [0, np.inf, 0], [0, 0, np.inf]],
            missing=None,
    )

    __model__ = _inertia.Inertia

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'InertiaSchema'
]
