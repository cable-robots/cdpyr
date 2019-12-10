from typing import Optional, Sequence

from magic_repr import make_repr

from cdpyr.kinematics.transformation import (
    angular as _angular,
    linear as _linear
)
from cdpyr.robot.anchor import anchor as _anchor
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformAnchor(_anchor.Anchor):

    def __init__(self,
                 position: Optional[Vector] = None,
                 dcm: Optional[Matrix] = None,
                 linear: Optional['_linear.Linear'] = None,
                 angular: Optional['_angular.Angular'] = None,
                 **kwargs):
        super().__init__(position, dcm, linear, angular, **kwargs)

    __repr__ = make_repr(
            'position',
            'dcm'
    )


class PlatformAnchorList(_anchor.AnchorList, RobotComponent):
    data: Sequence[PlatformAnchor]


__all__ = [
        'PlatformAnchor',
        'PlatformAnchorList',
]
