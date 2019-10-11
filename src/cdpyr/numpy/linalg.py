from typing import Union

import numpy as np_

from cdpyr.typing import Matrix, Num, Vector


def issquare(value: Union[Num, Vector, Matrix]):
    value = np_.asarray(value)

    return value.shape[0] == value.shape[1]
