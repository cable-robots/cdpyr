from marshmallow import Schema, fields

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Schema(Schema):
    class Meta:
        # ensures the order of fields is kept when exporting
        ordered = True

    version = fields.String(
            required=False,
            attribute='VERSION',
    )


class NamedSchema(Schema):
    name = fields.Function(
            lambda o: o.__class__.__name__.lower()
    )


__all__ = [
        'Schema',
        'NamedSchema',
]
