from abc import abstractmethod
from typing import Union

import numpy as _np
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.analysis import evaluator as _evaluator, result as _result
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.structure_matrix import calculator as _structure_matrix
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import robot as _robot
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Algorithm(_evaluator.PoseEvaluator):
    _force_minimum: Vector
    _force_maximum: Vector
    _structure_matrix: '_structure_matrix.Calculator'

    def __init__(self,
                 kinematics: '_kinematics.Algorithm',
                 force_minimum: Union[Num, Vector],
                 force_maximum: Union[Num, Vector],
                 **kwargs):
        super().__init__(**kwargs)
        self._structure_matrix = _structure_matrix.Calculator(kinematics)
        self.force_minimum = force_minimum
        self.force_maximum = force_maximum

    @property
    def force_maximum(self):
        return self._force_maximum

    @force_maximum.setter
    def force_maximum(self, force: Union[Num, Vector]):
        force = _np.asarray(force)
        if force.ndim == 0:
            force = _np.asarray([force])

        _validator.numeric.finite(force, 'force_maximum')

        self._force_maximum = force

    @force_maximum.deleter
    def force_maximum(self):
        del self._force_maximum

    @property
    def force_minimum(self):
        return self._force_minimum

    @force_minimum.setter
    def force_minimum(self, force: Union[Num, Vector]):
        force = _np.asarray(force)
        if force.ndim == 0:
            force = _np.asarray([force])

        _validator.numeric.nonnegative(force, 'force_minimum')

        self._force_minimum = force

    @force_minimum.deleter
    def force_minimum(self):
        del self._force_minimum

    def evaluate(self,
                 robot: '_robot.Robot',
                 pose: '_pose.Pose',
                 wrench: Vector,
                 **kwargs) -> 'Result':
        if robot.num_platforms > 1:
            raise NotImplementedError(
                    'Force distributions are currently not implemented for '
                    'robots '
                    'with more than one platform.'
            )

        # parse force limits
        force_min, force_max = self._parse_force_limits(robot)

        # get the structure matrix for the current pose
        structure_matrix = self._structure_matrix.evaluate(robot, pose)

        # pass down to actual implementation
        return self._evaluate(robot,
                              pose,
                              structure_matrix.matrix,
                              wrench,
                              force_min,
                              force_max,
                              **kwargs)

    @abstractmethod
    def _evaluate(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  structure_matrix: Matrix,
                  wrench: Vector,
                  force_min: Vector,
                  force_max: Vector,
                  **kwargs) -> 'Result':
        raise NotImplementedError()

    def _parse_force_limits(self, robot: '_robot.Robot'):
        # get configure force limits
        force_min = self._force_minimum
        force_max = self._force_maximum

        # fewer limits than kinematic chains passed
        if force_min.size < robot.num_kinematic_chains:
            force_min = _np.repeat(
                    force_min,
                    _np.ceil(robot.num_kinematic_chains / force_min.size)
            )[0:robot.num_kinematic_chains]
        if force_max.size < robot.num_kinematic_chains:
            force_max = _np.repeat(
                    force_max,
                    _np.ceil(robot.num_kinematic_chains / force_max.size)
            )[0:robot.num_kinematic_chains]

        # finally validate these values
        _validator.numeric.greater_than_or_equal_to(force_min,
                                                    0,
                                                    'force_min'
                                                    )
        _validator.numeric.less_than_or_equal_to(force_max,
                                                 _np.inf,
                                                 'force_max'
                                                 )

        return force_min, force_max


__all__ = [
        'Algorithm',
]


class Result(_result.PoseResult):
    _algorithm: 'Algorithm'
    _forces: Vector
    _wrench: Vector

    def __init__(self,
                 algorithm: 'Algorithm',
                 pose: '_pose.Pose',
                 forces: Vector,
                 wrench: Vector,
                 **kwargs):
        super().__init__(pose, **kwargs)
        self._algorithm = algorithm
        self._forces = forces
        self._wrench = wrench

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def forces(self):
        return self._forces

    @property
    def wrench(self):
        return self._wrench

    __repr__ = make_repr(
            'algorithm',
            'pose',
            'forces',
            'wrench'
    )


__all__ = [
        'Algorithm',
        'Result',
]
