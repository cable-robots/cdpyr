from typing import Sequence, Tuple, Union

from abc import ABC, abstractmethod
from magic_repr import make_repr

from cdpyr.motion import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Vector


class AlgorithmInterface(ABC):

    @classmethod
    @abstractmethod
    def forward(cls,
                robot: '_robot.Robot',
                lengths: Sequence[Vector]
                ) -> Union[Tuple[Vector, Matrix],
                           Tuple[Sequence[Vector], Sequence[Matrix]]]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def backward(cls,
                 robot: '_robot.Robot',
                 pose: Sequence['_pose.Pose']
                 ) -> Union[Tuple[Vector, Matrix],
                            Tuple[Sequence[Vector], Sequence[Matrix]]]:
        raise NotImplementedError()

    @classmethod
    def validate_inputs_forward(cls,
                                robot: '_robot.Robot',
                                lengths: Union[Sequence[Vector], Vector]):

        # we need as many cable lengths as we have kinematic chains
        if robot.num_kinematic_chains != len(lengths):
            raise ValueError(
                'Expected `{}` to have {} element{}, got {} instead.'.format(
                    'lengths',
                    robot.num_kinematic_chains,
                    's' if robot.num_kinematic_chains > 1 else '',
                    len(lengths)
                ))

    @classmethod
    def validate_inputs_backward(cls,
                                 robot: '_robot.Robot',
                                 pose: Sequence['_pose.Pose']):

        # we need as many pose as we have platforms
        if robot.num_platforms != len(pose):
            raise ValueError(
                'Expected `{}` to have {} element{}, got {} instead.'.format(
                    'pose',
                    robot.num_platforms,
                    's' if robot.num_platforms > 1 else '',
                    len(pose)
                ))


AlgorithmInterface.__repr__ = make_repr()

__all__ = [
    'AlgorithmInterface'
]
