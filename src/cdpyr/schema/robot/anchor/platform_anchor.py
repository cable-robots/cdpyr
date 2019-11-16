from marshmallow import fields, post_load

from cdpyr.robot.anchor import platform_anchor as _platform_anchor
from cdpyr.schema.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformAnchorSchema(_anchor.AnchorSchema):
    __model__ = _platform_anchor.PlatformAnchor

    @post_load(pass_many=True)
    def make_object(self, data, many, **kwargs):
        if many:
            return _platform_anchor.PlatformAnchorList(
                (self.make_object(each, False) for each in data))
        else:
            return self.__model__(**data)


__all__ = [
    'PlatformAnchorSchema',
]
