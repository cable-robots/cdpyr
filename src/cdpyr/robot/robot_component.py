from cdpyr.mixin.base_object import BaseObject

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class RobotComponent(BaseObject):

    @property
    def VERSION(self):
        return '1.0.0'


__all__ = [
        'RobotComponent',
]
