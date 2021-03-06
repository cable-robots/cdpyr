from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.numeric import greater_than_or_equal_to

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class GreaterThanOrEqualToTestSuite(object):

    def test_scalar_passes(self):
        greater_than_or_equal_to(1, 1)
        greater_than_or_equal_to(0, 0)
        greater_than_or_equal_to(-1, -1)

    def test_list_passes(self):
        greater_than_or_equal_to([1, 2, 3, 4], 1)
        greater_than_or_equal_to([1, 2, 3, 4], [1, 2, 3, 4])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            greater_than_or_equal_to([1, 2, 3, 4], 4)

        with pytest.raises(ValueError):
            greater_than_or_equal_to([1, 2, 3, 4], [2, 3, 4, 5])

    def test_list_of_list_passes(self):
        greater_than_or_equal_to(((1, 2), (3, 4)), 1)
        greater_than_or_equal_to(((1, 2), (3, 4)), ((1, 2), (3, 4)))

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            greater_than_or_equal_to(((1, 2), (3, 4)), 4)

        with pytest.raises(ValueError):
            greater_than_or_equal_to(((1, 2), (3, 4)), ((2, 3), (4, 5)))

    def test_numpyarray_passes(self):
        greater_than_or_equal_to(np.asarray((1, 2, 3, 4)), 1)
        greater_than_or_equal_to(np.asarray((1, 2, 3, 4)),
                                 np.asarray((1, 2, 3, 4)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            greater_than_or_equal_to(np.asarray((1, 2, 3, 4)), 4)

        with pytest.raises(ValueError):
            greater_than_or_equal_to(np.asarray((1, 2, 3, 4)),
                                     np.asarray((2, 3, 4, 5)))

    def test_numpyarray_passes(self):
        greater_than_or_equal_to(np.asarray(((1, 2), (3, 4))), 1)
        greater_than_or_equal_to(np.asarray(((1, 2), (3, 4))),
                                 np.asarray(((1, 2), (3, 4))))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            greater_than_or_equal_to(np.asarray(((1, 2), (3, 4))), 4)

        with pytest.raises(ValueError):
            greater_than_or_equal_to(np.asarray(((1, 2), (3, 4))),
                                     ((2, 3), (4, 5)))


if __name__ == "__main__":
    pytest.main()
