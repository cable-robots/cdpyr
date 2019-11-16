from typing import Optional, Sequence

from magic_repr import make_repr

from cdpyr.mixin.base_object import BaseObject
from cdpyr.robot import drivetrain as _drivetrain, pulley as _pulley
from cdpyr.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class FrameAnchor(_anchor.Anchor, BaseObject):
    _pulley: '_pulley.Pulley'
    _drivetrain: '_drivetrain.DriveTrain'

    def __init__(self,
                 *args,
                 pulley: Optional['_pulley.Pulley'] = None,
                 drivetrain: Optional['_drivetrain.DriveTrain'] = None,
                 **kwargs,
                 ):
        _anchor.Anchor.__init__(self, *args, **kwargs)
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

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.pulley == other.pulley and \
               self.drivetrain == other.drivetrain

    def __hash__(self):
        return hash((self.angular, self.drivetrain, self.linear, self.pulley))

    __repr__ = make_repr(
        'position',
        'dcm',
        'pulley',
        'drivetrain',
    )

class FrameAnchorList(_anchor.AnchorList):
    data: Sequence[FrameAnchor]

    @property
    def drivetrain(self):
        return (anchor.drivetrain for anchor in self.data)

    @property
    def pulley(self):
        return (anchor.pulley for anchor in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return all(this == that for this, that in zip(self, other))

    def __hash__(self):
        return hash(tuple(self.data))


__all__ = [
    'FrameAnchor',
    'FrameAnchorList',
]
