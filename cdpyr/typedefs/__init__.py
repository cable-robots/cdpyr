from typing import Sequence, Union

import numpy as np_

Num = Union[int, float]
Vector = Union[np_.ndarray, Sequence[Num]]
Matrix = Union[np_.ndarray, Sequence[Sequence[Num]]]

__all__ = [
    'Num',
    'Vector',
    'Matrix',
]
