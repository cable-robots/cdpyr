from cdpyr.visualization.plotly import (
    linear as _linear,
    planar as _planar,
    spatial as _spatial,
)
from cdpyr.visualization.plotly.plotly import Plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

LINEAR = _linear.Linear
PLANAR = _planar.Planar
SPATIAL = _spatial.Spatial

__all__ = [
    'Plotly',
    'LINEAR',
    'PLANAR',
    'SPATIAL',
]
