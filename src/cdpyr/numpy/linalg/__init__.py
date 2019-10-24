from typing import Union

import numpy as np_

from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def issquare(value: Union[Num, Vector, Matrix]):
    value = np_.asarray(value)

    return value.shape[0] == value.shape[1]


__all__ = [
    'issquare'
]
