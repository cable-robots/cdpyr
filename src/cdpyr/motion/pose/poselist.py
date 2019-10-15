from collections import UserList

from magic_repr import make_repr


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
    def transformationmatrix(self):
        return (pose.transformationmatrix for pose in self.data)

    @property
    def state(self):
        return (pose.state for pose in self.data)


PoseList.__repr__ = make_repr(
    'data'
)

__all__ = [
    'PoseList',
]
