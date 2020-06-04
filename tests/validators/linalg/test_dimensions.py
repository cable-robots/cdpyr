from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.linalg import dimensions

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class DimensionsTestSuite(object):

    def test_scalar_passes(self):
        dimensions(1, 0)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            dimensions(1, 1)

    def test_list_passes(self):
        dimensions((1, 2), 1)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            dimensions((1, 2), 2)

    def test_list_of_list_passes(self):
        dimensions(((1, 2), (3, 4)), 2)

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            dimensions(((1, 2), (3, 4)), 1)

    def test_numpyarray_passes(self):
        dimensions(np.asarray((1, 2)), 1)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            dimensions(np.asarray((1, 2)), 2)

    def test_numpyarray_passes(self):
        dimensions(np.asarray(((1, 2), (3, 4))), 2)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            dimensions(np.asarray(((1, 2), (3, 4))), 1)


if __name__ == "__main__":
    pytest.main()
