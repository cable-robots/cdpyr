from cdpyr.components.geometric import Cylinder


class Drum(Cylinder):

    def __init__(self, *args, **kwargs):
        Cylinder.__init__(self, *args, **kwargs)
