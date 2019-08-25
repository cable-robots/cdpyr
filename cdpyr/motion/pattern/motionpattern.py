from enum import Enum

from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.motion.pose import Pose
from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase
from cdpyr.motion.pattern._3r3t import _3R3T
from cdpyr.motion.pattern._2r3t import _2R3T
from cdpyr.motion.pattern._1r2t import _1R2T
from cdpyr.motion.pattern._1t import _1T
from cdpyr.motion.pattern._2t import _2T
from cdpyr.motion.pattern._3t import _3T


class Motionpattern(Enum):
    _1T = (_1T())
    _2T = (_2T())
    _3T = (_3T())
    _1R2T = (_1R2T())
    _2R3T = (_2R3T())
    _3R3T = (_3R3T())

    _pattern: MotionpatternBase

    # def __init__(self,
    #              pattern: MotionpatternBase
    #              ):
    #     self.pattern = pattern

    @property
    def translation(self):
        return self.value.translation

    @property
    def rotation(self):
        return self.value.rotation

    def moves_linear(self):
        return self.value.translation == 1 and self.value.rotation == 0

    def moves_planar(self):
        return self.value.translation == 2 and self.value.rotation == 1

    def move_spatial(self):
        return not self.is_planar()

    def is_point(self):
        return self.value.rotation == 0

    def is_beam(self):
        return 0 < self.value.rotation < self.value.translation

    def is_cuboid(self):
        return self.value.rotation == self.value.translation == 3

    def structure_matrix(self, pose: Pose):
        return self.value.structure_matrix(pose)


Motionpattern.__repr__ = make_repr(
    'translation',
    'rotation'
)


class MotionpatternSchema(Schema):
    translation = fields.Int()
    rotation = fields.Int()

    __model__ = Motionpattern

    @post_load
    def make_motionpattern(self, data):
        return self.__model__(**data)


__all__ = [
    'Motionpattern',
    'MotionpatternSchema',
]
