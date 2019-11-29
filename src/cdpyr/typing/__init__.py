from typing import Sequence, Union

import numpy as np_

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

Num = Union[int, float]
Vector = Union[Sequence[Num], np_.ndarray]
Matrix = Union[Sequence[Sequence[Num]], np_.ndarray]

__all__ = [
    'Num',
    'Vector',
    'Matrix',
]
