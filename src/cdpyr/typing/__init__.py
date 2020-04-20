__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Face',
        'Faces',
        'Matrix',
        'Num',
        'Vector',
        'Vertices',
        'Vertex',
]

from typing import Sequence, Tuple, Union

import numpy as _np

Num = Union[int, float]
Vector = Union[Sequence[Num], _np.ndarray]
Matrix = Union[Sequence[Sequence[Num]], _np.ndarray]
Vertex = Union[Tuple[float, float, float], _np.ndarray]
Vertices = Tuple[Vertex, ...]
Face = Union[Tuple[int, int, int], _np.ndarray]
Faces = Tuple[Face, ...]
