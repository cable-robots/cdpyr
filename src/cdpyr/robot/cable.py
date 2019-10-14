from typing import Optional, Sequence, Union

import numpy as np_
from colour import Color
from magic_repr import make_repr

from cdpyr.mixin.list import ObjectList
from cdpyr.typing import Num
from cdpyr import  validator as _validator


class Cable(object):
    _breaking_load: Num
    _color: Color
    _diameter: Num
    _material: str
    _modulus: dict
    _name: str

    def __init__(self,
                 name: Optional[str] = None,
                 material: Optional[str] = None,
                 modulus: Optional[dict] = None,
                 diameter: Optional[Num] = None,
                 color: Optional[Union[str, Color]] = None,
                 breaking_load: Optional[Num] = None
                 ):
        """ Base cable class that represents a rigid, elastic, viscous,
        or viscoelastic cable object.

        :rtype: Cable
        :param str name: Optional string representing a human-readable name of
        the cable
        :param str material: Optional string representing a human-readable
        name of the cable's material
        :param dict modulus: Optional dictionary mapping of elastic and viscous
        modulus of the cable. Contains the case-sensitive fields `elasticities`
        and `viscosities`
        :param float diameter: Optional float representing the cable's
        diameter in SI
        unit [ m ] (Meter)
        :param str|Color color: Optional string or Color object representing
        the object's color. Used mostly for visualizing the cable correctly.
        :param float|np_.Infinity breaking_load: Optional float or
        np_.Infinity representing the cable's rated breaking load. Set to
        `np_.Infinity` if the cable is like steel.
        """
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
    def diameter(self, diameter: Num):
        _validator.numeric.nonnegative(diameter, 'diameter')

        self._diameter = diameter

    @diameter.deleter
    def diameter(self):
        del self._diameter

    @property
    def breaking_load(self):
        return self._breaking_load

    @breaking_load.setter
    def breaking_load(self, breaking_load: Num):
        _validator.numeric.nonnegative(breaking_load, 'breaking_load')

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
    def elasticities(self, elasticities: Sequence[Num]):
        self.modulus['elasticities'] = elasticities

    @elasticities.deleter
    def elasticities(self):
        del self.modulus['elasticities']

    @property
    def viscosities(self):
        return self._modulus['viscosities']

    @viscosities.setter
    def viscosities(self, viscosities: Sequence[Num]):
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


class CableList(ObjectList):

    @property
    def __wraps__(self):
        return Cable

    def __dir__(self):
        return Cable.__dict__.keys()


__all__ = [
    'Cable',
    'CableList',
]
