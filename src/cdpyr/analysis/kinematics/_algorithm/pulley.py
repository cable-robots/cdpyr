from typing import Sequence, Tuple, Union

from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm.algorithm import Algorithm as \
    KinematicsInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class Pulley(KinematicsInterface):

    def forward(self,
                robot: '_robot.Robot',
                lengths: Sequence[Vector]
                ) -> Union[Tuple[Vector, Matrix],
                           Tuple[Sequence[Vector], Sequence[Matrix]]]:
        raise NotImplementedError()

    def backward(self,
                 robot: '_robot.Robot',
                 pose: Sequence['_pose.Pose']
                 ) -> Union[Tuple[Vector, Matrix],
                            Tuple[Sequence[Vector], Sequence[Matrix]]]:
        raise NotImplementedError()


Pulley.__repr__ = make_repr()

__all__ = [
    'Pulley'
]
