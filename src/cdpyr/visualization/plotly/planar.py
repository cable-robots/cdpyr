from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Planar(_plotly.Plotly):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 2
        self._NUMBER_OF_AXES = 2


__all__ = [
    'Planar',
]
