from typing import Optional, Sequence, Union

import numpy as np_
from colour import Color
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.mixins.lists import DispatcherList

_TNum = Union[int, float]
_TVector = Union[np_.ndarray, Sequence[_TNum]]
_TMatrix = Union[np_.ndarray, Sequence[Sequence[_TNum]]]


class Cable(object):
    _breaking_load: _TNum
    _color: Color
    _diameter: _TNum
    _material: str
    _modulus: dict
    _name: str

    def __init__(self,
                 name: Optional[str] = None,
                 material: Optional[str] = None,
                 modulus: Optional[dict] = None,
                 diameter: Optional[_TNum] = None,
                 color: Optional[Union[str, Color]] = None,
                 breaking_load: Optional[_TNum] = None
                 ):
        self.name = name or 'default'
        self.material = material or 'default'
        self.modulus = modulus or {}
        self.diameter = diameter or 0
        self.color = color or 'red'
        self.breaking_load = breaking_load or np_.Infinity

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter: _TNum):
        if diameter < 0:
            raise ValueError('diameter must be nonnegative')

        self._diameter = diameter

    @diameter.deleter
    def diameter(self):
        del self._diameter

    @property
    def breaking_load(self):
        return self._breaking_load

    @breaking_load.setter
    def breaking_load(self, breaking_load: _TNum):
        if breaking_load < 0:
            raise ValueError('breaking_load must be nonnegative')

        self._breaking_load = breaking_load

    @breaking_load.deleter
    def breaking_load(self):
        del self._breaking_load

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: str):
        self._material = material

    @material.deleter
    def material(self):
        del self._material

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Union[str, Color]):
        if not isinstance(color, Color):
            color = Color(color)

        self._color = color

    @color.deleter
    def color(self):
        del self._color

    @property
    def modulus(self):
        return self._modulus

    @modulus.setter
    def modulus(self, modulus: dict):
        default = {'elasticities': None, 'viscosities': None}
        modulus = modulus or {}

        self._modulus = {**default, **modulus}

    @modulus.deleter
    def modulus(self):
        del self._modulus

    @property
    def elasticities(self):
        return self._modulus['elasticities']

    @elasticities.setter
    def elasticities(self, elasticities: Sequence[_TNum]):
        self.modulus['elasticities'] = elasticities

    @elasticities.deleter
    def elasticities(self):
        del self.modulus['elasticities']

    @property
    def viscosities(self):
        return self._modulus['viscosities']

    @viscosities.setter
    def viscosities(self, viscosities: Sequence[_TNum]):
        self.modulus['viscosities'] = viscosities

    @viscosities.deleter
    def viscosities(self):
        del self.modulus['viscosities']


Cable.__repr__ = make_repr(
    'name',
    'material',
    'diameter',
    'modulus',
    'color',
    'breaking_load'
)


class CableSchema(Schema):
    name = fields.String()
    material = fields.String()
    diameter = fields.Float(required=True)
    modulus = fields.Dict(required=True)
    color = fields.String()
    breaking_load = fields.Float(required=True)

    __model__ = Cable

    @post_load
    def make_user(self, data):
        return self.__model__(**data)


class CableList(DispatcherList):

    def __dir__(self):
        return Cable.__dict__.keys()


__all__ = ['Cable', 'CableList', 'CableSchema']
