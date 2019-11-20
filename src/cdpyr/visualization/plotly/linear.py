from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Linear(_plotly.Plotly):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 1
        self._NUMBER_OF_AXES = 2

    def draw(self):
        self.figure.update_layout(
            yaxis=dict(
                showline=False,
                showticklabels=False,
                showgrid=False
            )
        )
        super().draw()


__all__ = [
    'Linear',
]
