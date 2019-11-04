from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.analysis.structure_matrix import calculator as _structure_matrix
from cdpyr.analysis.workspace.criterion import criterion as _criterion

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Singularities(_criterion.Criterion):
    _kinematics: '_kinematics.Algorithm'
    _structure_matrix: '_structure_matrix.Calculator'

    def __init__(self, kinematics: '_kinematics.Algorithm'):
        self.kinematics = kinematics
        if self.kinematics is not None:
            self._structure_matrix = _structure_matrix.Calculator(kinematics)

    @property
    def kinematics(self):
        return self._kinematics

    @kinematics.setter
    def kinematics(self, kinematics: '_kinematics.Algorithm'):
        self._kinematics = kinematics
        try:
            self._structure_matrix.kinematics = self._kinematics
        except AttributeError as AttributeE:
            self._structure_matrix = _structure_matrix.Calculator(
                self._kinematics)

    @kinematics.deleter
    def kinematics(self):
        del self._kinematics

    def _evaluate(self,
                  robot: '_robot.Robot',
                  pose: '_pose.Pose',
                  **kwargs):
        # according to Pott.2018, a pose is singular if the structure
        # matrix's rank is smaller than the number of degrees of freedom
        # i.e., the structure matrix's number of rows
        return self._structure_matrix.evaluate(robot, pose).is_singular

    def _validate(self, robot: '_robot.Robot'):
        if not isinstance(self.kinematics, _kinematics.Algorithm):
            raise AttributeError(
                f'Missing value for `kinematics` property. Please set a '
                f'kinematics algorithm on the `Singularities` object, '
                f'then calculate the workspace again')


__all__ = [
    'Singularities',
]
