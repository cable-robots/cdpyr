from magic_repr import make_repr

from cdpyr.analysis.kinematics._algorithm.algorithm import Algorithm as \
    KinematicsInterface
from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot


class Pulley(KinematicsInterface):

    def forward(self,
                robot: '_robot.Robot',
                pose: '_pose.Pose'
                ):
        raise NotImplementedError()

    def backward(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose'
                 ):
        raise NotImplementedError()


Pulley.__repr__ = make_repr()

__all__ = [
    'Pulley'
]
