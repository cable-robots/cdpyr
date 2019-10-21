from cdpyr.analysis.workspace import workspace as _calculator
from cdpyr.analysis.workspace.criterion import criterion as _criterion
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot

__vars__ = [
]


def setup(criterion: '_criterion.Criterion',
          robot: '_robot.Robot'):
    pass


def teardown(criterion: '_criterion.Criterion',
             robot: '_robot.Robot'):
    pass


def evaluate(criterion: '_criterion.Criterion',
             robot: '_robot.Robot',
             calculator: '_calculator.Calculator',
             pose: '_pose.Pose'):
    raise NotImplementedError
