from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.linalg import square

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class SquareTestSuite(object):

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            square(1)

    def test_list_passes(self):
        square(np.random.random((3, 3)).tolist())

    def test_list_fails(self):
        with pytest.raises(ValueError):
            square(np.random.random((2,)).tolist())

        with pytest.raises(ValueError):
            square(np.random.random((2, 3)).tolist())

        with pytest.raises(ValueError):
            square(np.random.random((2, 3, 4)).tolist())

    def test_numpyarray_passes(self):
        square(np.random.random((3, 3)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            square(np.random.random((2,)))

        with pytest.raises(ValueError):
            square(np.random.random((2, 3)))

        with pytest.raises(ValueError):
            square(np.random.random((2, 3, 4)))


if __name__ == "__main__":
    pytest.main()
