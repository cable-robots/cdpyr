from enum import Enum

from magic_repr import make_repr

from cdpyr.typing import Num


class Motionpattern(Enum):
    _1T = (1, 0, '1T')
    _2T = (2, 0, '2T')
    _3T = (3, 0, '3T')
    _1R2T = (2, 1, '1R2T')
    _2R3T = (3, 2, '2R3T')
    _3R3T = (3, 3, '3R3T')

    _dof_translation: int
    _dof_rotation: int
    _human: str

    def __init__(self,
                 translation: Num,
                 rotation: Num,
                 name: str):
        self._dof_translation = translation
        self._dof_rotation = rotation
        self._human = name

    @property
    def dof_translation(self):
        return self._dof_translation

    @property
    def dof_rotation(self):
        return self._dof_rotation

    @property
    def human(self):
        return self._human

    @property
    def moves_linear(self):
        return self.dof_translation == 1 and self.dof_rotation == 0

    @property
    def moves_planar(self):
        return self.dof_translation == 2 and self.dof_rotation == 1

    @property
    def moves_spatial(self):
        return not self.is_planar

    @property
    def is_point(self):
        return self.dof_rotation == 0

    @property
    def is_beam(self):
        return 0 < self.dof_rotation < self.dof_translation

    @property
    def is_cuboid(self):
        return self.dof_rotation == self.dof_translation == 3


Motionpattern.__repr__ = make_repr(
    'human',
    'dof_translation',
    'dof_rotation',
)

__all__ = [
    'Motionpattern',
]
