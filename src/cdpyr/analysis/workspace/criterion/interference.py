from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.workspace.criterion import criterion as _criterion

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Interference(_criterion.Criterion):
    _kinematics: '_kinematics.Algorithm'

    def __init__(self, kinematics: '_kinematics.Algorithm'):
        self.kinematics = kinematics

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Algorithm'):
        self._kinematics = kinematics

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

    def _evaluate(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs):
        raise NotImplementedError

    def _validate(self, robot: '_robot.Robot'):
        if not isinstance(self.kinematics, _kinematics.Algorithm):
            raise AttributeError(
                f'Missing value for `kinematics` property. Please set a '
                f'kinematics algorithm on the `Interference` object, '
                f'then calculate the workspace again')


__all__ = [
    'Interference',
]
