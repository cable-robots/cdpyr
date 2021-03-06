from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.linalg import inertia_tensor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class InertiaTensorTestSuite(object):

    def test_list_passes(self):
        inertia_tensor([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            inertia_tensor([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])

    def test_numpyarray_passes(self):
        inertia_tensor(np.asarray((
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        )))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            inertia_tensor(np.asarray((
                (-1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )))


if __name__ == "__main__":
    pytest.main()
