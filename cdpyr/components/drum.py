from cdpyr.traits.geometric import Cylindric


class Drum(object, Cylindric):

    def __init__(self, radius: float = None, mass: float = None, length:
    float = None):
        super().__init__(radius=radius, length=length, mass=mass)
