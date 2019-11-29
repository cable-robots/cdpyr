from cdpyr.visualization.engine.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Linear(_plotly.Plotly):
    _NUMBER_OF_COORDINATES = 1
    _NUMBER_OF_AXES = 2

    def draw(self, *args, **kwargs):
        super().draw()
        self.figure.update_layout(
                yaxis=dict(
                        scaleanchor="x",
                        scaleratio=1,
                        showline=False,
                        showticklabels=False,
                        showgrid=False
                ),
                **kwargs
        )


__all__ = [
    'Linear',
]
#
