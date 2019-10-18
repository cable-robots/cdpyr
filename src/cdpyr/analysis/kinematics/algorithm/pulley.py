from typing import Sequence

from cdpyr.analysis.kinematics.calculator import calculator as _calculator
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Vector


def forward(calculator: '_calculator.Calculator',
            robot: '_robot.Robot',
            joints: Sequence[Vector]):
    pass


def backward(calculator: '_calculator.Calculator',
             robot: '_robot.Robot',
             pose: Sequence['_pose.Pose']):
    pass
