from cdpyr.visualization.matplotlib import (
    linear as _linear,
    planar as _planar,
    spatial as _spatial,
)
from cdpyr.visualization.matplotlib.matplotlib import Matplotlib

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

LINEAR = _linear.Linear
PLANAR = _planar.Planar
SPATIAL = _spatial.Spatial

__all__ = [
    'Matplotlib',
    'LINEAR',
    'PLANAR',
    'SPATIAL',
]
