from collections import UserList

from magic_repr import make_repr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseList(UserList):

    @property
    def time(self):
        return (pose.time for pose in self.data)

    @property
    def position(self):
        return (pose.position for pose in self.data)

    @property
    def velocity(self):
        return (pose.velocity for pose in self.data)

    @property
    def acceleration(self):
        return (pose.acceleration for pose in self.data)

    @property
    def linear(self):
        return (pose.linear for pose in self.data)

    @property
    def angular(self):
        return (pose.angular for pose in self.data)

    @property
    def transformation(self):
        return (pose.transformation for pose in self.data)

    @property
    def state(self):
        return (pose.state for pose in self.data)

    __repr__ = make_repr(
        'data'
    )


__all__ = [
    'PoseList',
]
