from enum import Enum

from cdpyr.motion.pose import Pose
from cdpyr.robot.robot import Robot


class Kinetostatics(Enum):
    STANDARD = 'standard'
    PULLEY = 'pulley'
    CATENARY = 'catenary'
    ELASTIC_CATENARY = 'catenary'

    def forward(self, robot: Robot, pose: Pose):
        raise NotImplementedError()

    def backward(self, robot: Robot, pose: Pose):
        raise NotImplementedError()

    def _backward_standard(self):
        pass

    def _backward_pulley(self):
        pass

    def _backward_catenary(self):
        pass

    def _backward_elastic_catenary(self):
        pass

    def _forward_standard(self):
        pass

    def _forward_pulley(self):
        pass

    def _forward_catenary(self):
        pass

    def _forward_elastic_catenary(self):
        pass

__all__ = [
    'Kinetostatics'
]
