from typing import Sequence, Tuple, Union

from enum import Enum
from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm import (
    Algorithm as KinematicsAlgorithm,
    Pulley,
    Standard,
)
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class Kinematics(Enum):
    STANDARD = (Standard())
    PULLEY = (Pulley())

    @property
    def algorithm(self) -> KinematicsAlgorithm:
        return self._value_

    def forward(self,
                robot: '_robot.Robot',
                lengths: Union[Sequence[Vector], Vector]
                ) -> Union[Tuple[Vector, Matrix],
                           Tuple[Sequence[Vector], Sequence[Matrix]]]:
        lengths = lengths if isinstance(lengths, Sequence) else [lengths]

        self.algorithm.validate_inputs_forward(robot, lengths)

        return self.algorithm.forward(robot, lengths)

    def backward(self,
                 robot: '_robot.Robot',
                 pose: Union[Sequence['_pose.Pose'], '_pose.Pose']
                 ) -> Union[Tuple[Vector, Matrix],
                            Tuple[Sequence[Vector], Sequence[Matrix]]]:
        pose = pose if isinstance(pose, Sequence) else [pose]

        self.algorithm.validate_inputs_backward(robot, pose)

        return self.algorithm.backward(robot, pose)


Kinematics.__repr__ = make_repr()

__all__ = [
    'Kinematics'
]
