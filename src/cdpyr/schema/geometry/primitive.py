from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'PrimitiveSchema',
]

from abc import abstractmethod

from marshmallow import post_load, Schema


class PrimitiveSchema(Schema):

    @property
    @abstractmethod
    def __model__(self):
        raise NotImplementedError()

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
