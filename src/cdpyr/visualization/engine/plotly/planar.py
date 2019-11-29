from cdpyr.visualization.engine.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Planar(_plotly.Plotly):
    _NUMBER_OF_COORDINATES = 2
    _NUMBER_OF_AXES = 2

    def draw(self, *args, **kwargs):
        super().draw()
        self.figure.update_layout(
                yaxis=dict(
                        scaleanchor="x",
                        scaleratio=1,
                ),
                scene=dict(
                        aspectmode='data',
                        aspectratio=dict(
                                x=1.00,
                                y=1.00,
                                z=1.00
                        )
                ),
                **kwargs
        )


__all__ = [
    'Planar',
]
