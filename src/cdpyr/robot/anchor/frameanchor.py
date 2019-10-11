from typing import Optional, Union

from magic_repr import make_repr

from cdpyr.kinematics.transformation.angular import \
    Angular as AngularTransformation
from cdpyr.kinematics.transformation.linear import Linear as \
    LinearTransformation
from cdpyr.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.robot.anchor import anchor as _anchor
from cdpyr.typing import Matrix, Vector


class FrameAnchor(_anchor.Anchor):
    _pulley: '_pulley.Pulley'
    _drivetrain: '_drivetrain.DriveTrain'

    def __init__(self,
                 position: Optional[
                     Union[Vector, LinearTransformation]] = None,
                 rotation: Optional[
                     Union[Matrix, AngularTransformation]] = None,
                 pulley: Optional['_pulley.Pulley'] = None,
                 drivetrain: Optional['_drivetrain.DriveTrain'] = None
                 ):
        _anchor.Anchor.__init__(self, position=position, rotation=rotation)
        self.pulley = pulley or None
        self.drivetrain = drivetrain or None

    @property
    def pulley(self):
        return self._pulley

    @pulley.setter
    def pulley(self, pulley: '_pulley.Pulley'):
        self._pulley = pulley

    @pulley.deleter
    def pulley(self):
        del self._pulley

    @property
    def drivetrain(self):
        return self._drivetrain

    @drivetrain.setter
    def drivetrain(self, drivetrain: '_drivetrain.DriveTrain'):
        self._drivetrain = drivetrain

    @drivetrain.deleter
    def drivetrain(self):
        del self._drivetrain


FrameAnchor.__repr__ = make_repr(
    'position',
    'dcm',
    'pulley',
    'drivetrain'
)


# class FrameAnchorSchema(_anchor.AnchorSchema):
#     pulley = fields.Nested(_pulley.PulleySchema)
#     drivetrain = fields.Nested(_drivetrain.DriveTrainSchema)
#
#     __model__ = FrameAnchor


class FrameAnchorList(_anchor.AnchorList):

    @property
    def __wraps__(self):
        return FrameAnchor

    def __dir__(self):
        return FrameAnchor.__dict__.keys()


__all__ = [
    'FrameAnchor',
    'FrameAnchorList',
    # 'FrameAnchorSchema',
]
