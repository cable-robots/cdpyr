from cdpyr.algorithms.kinematics.algorithm import KinematicAlgorithm
from cdpyr.algorithms.kinematics.pulley import PulleyKinematics
from cdpyr.algorithms.kinematics.solver import KinematicsSolver
from cdpyr.algorithms.kinematics.standard import StandardKinematics

__all__ = ['KinematicAlgorithm',
           'KinematicsSolver',
           'StandardKinematics',
           'PulleyKinematics'
           ]

# class Kinematics(Enum):
#     STANDARD = 'standard'
#     PULLEY = 'pulley'
#
#     @property
#     def algorithm(self):
#         return self.value
#
#     def forward(self, robot: Robot, pose: Pose):
#         f, _ = self._resolve_function()
#
#         return f(
#             pose=pose.position,
#             ai=robot.ai,
#             bi=robot.bi,
#         )
#
#     def backward(self, robot: Robot, pose: Pose):
#         _, f = self._resolve_function()
#
#         return f(
#             pose=pose.position,
#             ai=robot.ai,
#             bi=robot.bi,
#         )
#
#     def _resolve_function(self):
#         _FUNC_MAPPING = {
#             'standard': (self._forward_standard, self._backward_standard),
#             'pulley': (self._forward_pulley, self._backward_pulley),
#         }
#
#         return _FUNC_MAPPING[self.value]
#
#     def _backward_standard(self,
#                            pose: Tuple[_TVector, _TMatrix],
#                            ai: Sequence[FrameAnchor],
#                            bi: Sequence[PlatformAnchor]
#                            ):
#         raise NotImplementedError()
#
#     def _backward_pulley(self,
#                          pose: Tuple[_TVector, _TMatrix],
#                          ai: Sequence[FrameAnchor],
#                          bi: Sequence[PlatformAnchor]
#                          ):
#         raise NotImplementedError()
#
#     def _forward_standard(self,
#                           pose: Tuple[_TVector, _TMatrix],
#                           ai: Sequence[FrameAnchor],
#                           bi: Sequence[PlatformAnchor]
#                           ):
#         raise NotImplementedError()
#
#     def _forward_pulley(self,
#                         pose: Tuple[_TVector, _TMatrix],
#                         ai: Sequence[FrameAnchor],
#                         bi: Sequence[PlatformAnchor]
#                         ):
#         raise NotImplementedError()
#
#
# Kinematics.__repr__ = make_repr('algorithm')
#
# __all__ = ['Kinematics']
