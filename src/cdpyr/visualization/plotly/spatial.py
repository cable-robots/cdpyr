from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Spatial(_plotly.Plotly):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 3
        self._NUMBER_OF_AXES = 3


__all__ = [
    'Spatial',
]
