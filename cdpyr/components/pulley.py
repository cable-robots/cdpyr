from cdpyr.traits.angularkinematics import AngularKinematics


class Pulley(object, AngularKinematics):

    def __init__(self, orientation=None):
        super().__init__(orientation=orientation)
        self.radius = 1
        self.material = 'default'

    @property
    def diameter(self):
        return 2 * self.radius

    @diameter.setter
    def diameter(self, d):
        if d <= 0:
            raise ValueError('diameter must be positive')

        self.radius = d / 2
