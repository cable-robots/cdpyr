from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.numeric import positive

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PositiveTestSuite(object):

    def test_scalar_passes(self):
        positive(4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            positive(-4)
        with pytest.raises(ValueError):
            positive(0)

    def test_list_passes(self):
        positive((1, 2, 3, 4))

    def test_list_fails(self):
        with pytest.raises(ValueError):
            positive([0, 0, 0, 0])

        with pytest.raises(ValueError):
            positive([-1, -2, -3, -4])

    def test_tuple_passes(self):
        positive((1, 2, 3, 4))

    def test_tuple_fails(self):
        with pytest.raises(ValueError):
            positive((0, 0, 0, 0))

        with pytest.raises(ValueError):
            positive((-1, -2, -3, -4))

    def test_numpy_vector_passes(self):
        positive(np.asarray((1, 2, 3, 4)))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            positive((0, 0, 0, 0))

        with pytest.raises(ValueError):
            positive((-1, -2, -3, -4))


if __name__ == "__main__":
    pytest.main()
