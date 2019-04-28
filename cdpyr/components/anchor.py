from cdpyr.traits.orientable import Orientable
from cdpyr.traits.positionable import Positionable


class Anchor(object, Orientable, Positionable):

    def __init__(self, position: None, orientation: None):
        super().__init__(position=position)
        super().__init__(orientation=orientation)
    
