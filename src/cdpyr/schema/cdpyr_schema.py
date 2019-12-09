from marshmallow import Schema, fields

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class CdpyrSchema(Schema):
    class Meta:
        # ensures the order of fields is kept when exporting
        ordered = True

    version = fields.String(
            required=False,
            attribute='VERSION',
    )
    # version_out = fields.Raw(
    #         required=False,
    #         dump_only=True,
    #         attribute='version'
    # )
    # version_in = fields.Raw(
    #         required=False,
    #         load_only=True,
    #         data_key='version'
    # )


__all__ = [
        'CdpyrSchema',
]
