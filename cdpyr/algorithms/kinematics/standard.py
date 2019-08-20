from magic_repr import make_repr

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class StandardKinematics(object):

    def forward(self,
                robot: Robot,
                pose: Pose
                ):
        raise NotImplementedError

    def backward(self,
                 robot: Robot,
                 pose: Pose
                 ):
        raise NotImplementedError


StandardKinematics.__repr__ = make_repr()

__all__ = [
    'StandardKinematics'
]
