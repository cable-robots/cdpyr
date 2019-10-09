import numpy as np
import pytest

from cdpyr.validator import inertia_tensor


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
