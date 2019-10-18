from typing import Sequence, Union

from enum import Enum

from cdpyr import validator as _validator
from cdpyr.analysis.kinematics.algorithm import pulley, standard
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Vector


class Calculator(Enum):
    STANDARD = [standard]
    PULLEY = [pulley]

    @property
    def implementation(self):
        return self._value_[0]

    def forward(self,
                robot: '_robot.Robot',
                joints: Union[Vector, Sequence[Vector]]):
        # ensure consistent data for the underlying implementation
        joints = joints if isinstance(joints, Sequence) else [joints]

        # validate number of joints matches the number of platforms
        _validator.data.length(joints, robot.num_platforms, 'joints')
        # ensure each platform gets as many cable lengths as it has kinematic
        # chains
        [_validator.data.length(joints[idx],
                                len(robot.kinematic_chains.with_platform(platform)),
                                'joints[{}]'.format(idx)) for idx, platform in
         robot.platforms]

        # and delegate to the underlying implementation
        return self.implementation.forward(self, robot, joints)

    def backward(self,
                 robot: '_robot.Robot',
                 pose: Union['_pose.Pose', Sequence['_pose.Pose']]
                 ):
        # ensure consistent data for the underlying implementation
        pose = pose if isinstance(pose, Sequence) else [pose]

        # validate the number of poses matches the number of platforms
        _validator.data.length(pose, robot.num_platforms, 'pose')

        # and delegate to the underlying implementation
        return self.implementation.backward(self, robot, pose)


__all__ = [
    'Calculator',
]
