from collections import UserList
from typing import Sequence, Union

import numpy as np_
from magic_repr import make_repr
from marshmallow import Schema, fields, post_load

from cdpyr.motion.pose import Pose, PoseSchema

from cdpyr.typedefs import Num, Vector, Matrix


class PoseList(UserList):
    data: Sequence[Pose]

    def __init__(self, poses: None):
        super().__init__(self)
        self.data = poses or []

    @property
    def poses(self):
        return self.data

    @poses.setter
    def poses(self, poses: Sequence[Pose]):
        self.data = poses

    @poses.deleter
    def poses(self):
        del self.data


PoseList.__repr__ = make_repr(
    'poses'
)


class PoseListSchema(Schema):
    poses = fields.List(fields.Nested(PoseSchema))

    __model__ = PoseList

    @post_load
    def make_poselist(self, data):
        return self.__model__(**data)


__all__ = ['PoseList', 'PoseListSchema']
