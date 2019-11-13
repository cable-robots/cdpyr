from cdpyr.visualization.matplotlib import matplotlib as _matplotlib

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Spatial(_matplotlib.Matplotlib):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 3
        self._NUMBER_OF_AXES = 3


__all__ = [
    'Spatial',
]
