from collections import UserList
from typing import AnyStr, Dict, Optional, Union

import numpy as _np
from colour import Color
from magic_repr import make_repr

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Cable(RobotComponent):
    breaking_load: Num
    _color: Color
    density: Num
    diameter: Num
    _lengths: Dict[AnyStr, Num]
    material: AnyStr
    _modulus: Dict[AnyStr, Vector]
    name: AnyStr

    def __init__(self,
                 name: Optional[AnyStr] = None,
                 material: Optional[AnyStr] = None,
                 modulus: Optional[Dict[AnyStr, Vector]] = None,
                 diameter: Optional[Num] = None,
                 color: Optional[Union[AnyStr, Color]] = None,
                 breaking_load: Optional[Num] = None,
                 density: Num = None,
                 lengths: Dict[AnyStr, Num] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.name = name or 'default'
        self.material = material or 'default'
        self.modulus = modulus or {}
        self.diameter = diameter or 0
        self.color = color or 'red'
        self.breaking_load = breaking_load or _np.Infinity
        self.density = density or _np.Infinity
        self.lengths = lengths or {}

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Union[AnyStr, Color]):
        if not isinstance(color, Color):
            color = Color(color)

        self._color = color

    @color.deleter
    def color(self):
        del self._color

    @property
    def lengths(self):
        return self._lengths

    @lengths.setter
    def lengths(self, lengths: Dict[AnyStr, Num]):
        self._lengths = {**{'min': 0, 'max': _np.Infinity}, **lengths};

    @property
    def modulus(self):
        return self._modulus

    @modulus.setter
    def modulus(self, modulus: Dict[AnyStr, Vector]):
        self._modulus = {**{'elasticities': None, 'viscosities': None},
                         **modulus}

    @modulus.deleter
    def modulus(self):
        del self._modulus

    @property
    def elasticities(self):
        return self._modulus['elasticities']

    @elasticities.setter
    def elasticities(self, elasticities: Vector):
        if elasticities is not None:
            elasticities = _np.asarray(elasticities)
        self.modulus['elasticities'] = elasticities

    @elasticities.deleter
    def elasticities(self):
        del self.modulus['elasticities']

    @property
    def viscosities(self):
        return self._modulus['viscosities']

    @viscosities.setter
    def viscosities(self, viscosities: Vector):
        if viscosities is not None:
            viscosities = _np.asarray(viscosities)
        self.modulus['viscosities'] = viscosities

    @viscosities.deleter
    def viscosities(self):
        del self.modulus['viscosities']

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.breaking_load == other.breaking_load \
               and self.color == other.color \
               and self.diameter == other.diameter \
               and self.material == other.material \
               and self.modulus == other.modulus \
               and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.breaking_load,
                     self.color.get_hex(),
                     self.diameter,
                     self.material,
                     frozenset(self.modulus.items()),
                     self.name))

    __repr__ = make_repr(
            'name',
            'material',
            'diameter',
            'lengths',
            'modulus',
            'color',
            'breaking_load',
    )


class CableList(UserList, RobotComponent):

    @property
    def name(self):
        return (cable.name for cable in self.data)

    @property
    def material(self):
        return (cable.material for cable in self.data)

    @property
    def diameter(self):
        return (cable.diameter for cable in self.data)

    @property
    def modulus(self):
        return (cable.modulus for cable in self.data)

    @property
    def color(self):
        return (cable.color for cable in self.data)

    @property
    def breaking_load(self):
        return (cable.breaking_load for cable in self.data)

    @property
    def elasticities(self):
        return (cable.elasticities for cable in self.data)

    @property
    def viscosities(self):
        return (cable.viscosities for cable in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.data))

    __repr__ = make_repr(
            'data'
    )


__all__ = [
        'Cable',
        'CableList',
]
