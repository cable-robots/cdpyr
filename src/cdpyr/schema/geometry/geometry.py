from abc import abstractmethod

from marshmallow import Schema, fields, post_load

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GeometrySchema(Schema):
    @property
    @abstractmethod
    def __model__(self):
        raise NotImplementedError()

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'GeometrySchema',
]
