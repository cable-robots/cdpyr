from cdpyr.traits.angularkinematics import AngularKinematics
from cdpyr.traits.linearkinematics import LinearKinematics


class Anchor(object, AngularKinematics, LinearKinematics):

    def __init__(self, position: None, orientation: None):
        super().__init__(position=position)
        super().__init__(orientation=orientation)
    
