from cdpyr.visualization.matplotlib import matplotlib as _matplotlib

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Linear(_matplotlib.Matplotlib):
    _NUMBER_OF_COORDINATES = 1
    _NUMBER_OF_AXES = 2

    def draw(self):
        self._axes().yaxis.set_visible(False)
        super().draw()


__all__ = [
    'Linear',
]
