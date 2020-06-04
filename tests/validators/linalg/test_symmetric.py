from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.linalg import symmetric

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class SymmetricTestSuite(object):

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            symmetric(1)

    def test_list_passes(self):
        symmetric([
            [1, 2, 3],
            [2, 4, 5],
            [3, 5, 6]
        ])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            symmetric([
                [1, 2, 3],
                [2, 3, 1],
                [3, 2, 1]
            ])

    def test_numpyarray_passes(self):
        symmetric(np.asarray((((1, 2, 3), (2, 4, 5), (3, 5, 6)))))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            symmetric(np.asarray((
                (1, 2, 3),
                (2, 3, 1),
                (3, 2, 1)
            )))


if __name__ == "__main__":
    pytest.main()
