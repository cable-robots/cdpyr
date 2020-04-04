from __future__ import annotations

from typing import AnyStr, Optional, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr.base import Object
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Pattern(Object):
    _dof_translation: int
    _dof_rotation: int
    _human: AnyStr

    def __init__(self,
                 translation: Num,
                 rotation: Num,
                 **kwargs):
        super().__init__(**kwargs)
        self._dof_translation = translation
        self._dof_rotation = rotation

    @property
    def dof_translation(self):
        return self._dof_translation

    @property
    def dof_rotation(self):
        return self._dof_rotation

    @property
    def dof(self):
        return self.dof_translation + self.dof_rotation

    @property
    def human(self):
        return f'{self.dof_rotation if self.dof_rotation else ""}' \
               f'{"R" if self.dof_rotation else ""}' \
               f'{self.dof_translation}T'

    @property
    def moves_linear(self):
        return self.dof_translation == 1

    @property
    def moves_planar(self):
        return self.dof_translation == 2

    @property
    def moves_spatial(self):
        return self.dof_translation == 3

    @property
    def can_rotate(self):
        return self.dof_rotation > 0

    @property
    def is_point(self):
        return self.dof_rotation == 0

    @property
    def is_beam(self):
        return 0 < self.dof_rotation < self.dof_translation

    @property
    def is_cuboid(self):
        return self.dof_rotation == self.dof_translation == 3

    def gravity(self, gravity: Optional[Union[Num, Vector]]):
        # first, scalar value for gravity
        gravity = np_.asarray(gravity if gravity is not None else 0)

        # ensure we have a 1-dim vector
        if gravity.ndim == 0:
            gravity = np_.asarray([gravity])

        # then make the gravity scalar match the linear DOF of the platform.
        # By convention, we will add the scalar gravity value to the last DOF
        # of translation
        return np_.pad(gravity, (self.dof_translation - gravity.size, 0))

    def gravitational_wrench(self,
                             linear_inertia: Matrix,
                             gravity: Vector,
                             rot: Optional[Matrix] = None,
                             cog: Optional[Vector] = None):
        # default value for rotation
        rot = np_.asarray(rot) if rot is not None else np_.eye(3)

        # default value for center of gravity
        cog = np_.asarray(cog) if cog is not None else np_.zeros(
                self.dof_translation)

        gravity: Vector
        linear_inertia: Matrix
        cog: Vector
        rot: Matrix
        # reduce dimensions of vectors and matrices for quicker calculations
        gravity = gravity[0:self.dof_translation]
        linear_inertia = linear_inertia[0:self.dof_translation,
                         0:self.dof_translation]
        rot = rot[0:(self.dof_rotation + 1), 0:(self.dof_rotation + 1)]
        cog = cog[0:self.dof_translation]

        # wrench that acts on the platform is composed of the gravitational
        # forces (quite simply linear inertia multiplied by vector of
        # gravity) and of the torques generated by the center of gravity offset
        if self.dof_rotation > 1:
            return np_.hstack((
                    linear_inertia.dot(gravity),
                    np_.cross(rot.dot(cog),
                              linear_inertia.dot(gravity))[0:self.dof_rotation]
            ))
        elif self.dof_rotation == 1:
            return np_.hstack((
                    linear_inertia.dot(gravity),
                    np_.cross(rot.dot(cog), linear_inertia.dot(gravity))
            ))
        else:  # no rotation, just linear motion
            return linear_inertia.dot(gravity)

    def __hash__(self):
        return hash((self.dof_rotation, self.dof_translation))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return self.dof_translation == other.dof_translation \
               and self.dof_rotation == other.dof_rotation

    def __ne__(self, other):
        return not self == other

    __repr__ = make_repr(
            'human',
            'dof_translation',
            'dof_rotation',
    )


MP_1T = Pattern(1, 0)
MP_2T = Pattern(2, 0)
MP_3T = Pattern(3, 0)
MP_1R2T = Pattern(2, 1)
MP_2R3T = Pattern(3, 2)
MP_3R3T = Pattern(3, 3)

__all__ = [
        'MP_1T',
        'MP_2T',
        'MP_3T',
        'MP_1R2T',
        'MP_2R3T',
        'MP_3R3T',
]
