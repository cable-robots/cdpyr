import itertools
from typing import Optional

import numpy as _np
from plotly import graph_objects as go
from scipy.spatial import Delaunay as _Delaunay

from cdpyr.analysis.workspace import (
    grid as _grid,
    hull as _hull
)
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.typing import (
    Matrix,
    Num
)
from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Spatial(_plotly.Plotly):
    _NUMBER_OF_COORDINATES = 3
    _NUMBER_OF_AXES = 3


__all__ = [
    'Spatial',
]
