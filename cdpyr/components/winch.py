from cdpyr.components.geometric import Cylinder
from cdpyr.components.drum import Drum


class Winch(Cylinder):

    _drum: Drum

    def __init__(self, *args, **kwargs):
        Cylinder.__init__(self, *args, **kwargs)

    @property
    def drum(self):
        return self._drum

    @drum.setter
    def drum(self, drum: Drum):
        self._drum = drum
