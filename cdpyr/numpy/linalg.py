from typing import Iterable
from typing import Union

import numpy as np_


def skewmatrix(a: Union[list, np_.ndarray, Iterable, int, float]):
    a = np_.asarray(a, dtype=np_.float64)

    skv: np_.ndarray = np_.roll(np_.roll(np_.diag(a.flatten()), 1, 1), -1, 0)

    return skv - skv.T
