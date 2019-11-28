from cdpyr.visualization.matplotlib import matplotlib as _matplotlib

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Planar(_matplotlib.Matplotlib):
    _NUMBER_OF_COORDINATES = 2
    _NUMBER_OF_AXES = 2


__all__ = [
    'Planar',
]
