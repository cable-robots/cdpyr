from typing import Union

import numpy as np_


class Positionable(object):

    def __init__(self, position: Union[np_.ndarray, list] = None):
        self.position = position if position is not None else np_.zeros(3)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p: Union[np_.ndarray, list]):
        if not isinstance(p, np_.ndarray):
            p = np_.array(p, dtype=np_.float64)

        if not p.shape == (3,):
            raise ValueError('position must be of shape (3, )')

        self._position = p
