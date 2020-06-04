from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.numeric import less_than_or_equal_to

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class LessThanOrEqualToTestSuite(object):

    def test_scalar_passes(self):
        less_than_or_equal_to(0, 0)
        less_than_or_equal_to(1, 1)
        less_than_or_equal_to(-1, -1)

    def test_list_passes(self):
        less_than_or_equal_to([1, 2, 3, 4], 4)
        less_than_or_equal_to([1, 2, 3, 4], [1, 2, 3, 4])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to([1, 2, 3, 4], 1)
        with pytest.raises(ValueError):
            less_than_or_equal_to([1, 2, 3, 4], [0, 1, 2, 3])

    def test_list_of_list_passes(self):
        less_than_or_equal_to(((1, 2), (3, 4)), 4)
        less_than_or_equal_to(((1, 2), (3, 4)), ((1, 2), (3, 4)))

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(((1, 2), (3, 4)), 1)

        with pytest.raises(ValueError):
            less_than_or_equal_to(((1, 2), (3, 4)), ((0, 1), (2, 3)))

    def test_numpyarray_passes(self):
        less_than_or_equal_to(np.asarray((1, 2, 3, 4)), 4)
        less_than_or_equal_to(np.asarray((1, 2, 3, 4)),
                              np.asarray((1, 2, 3, 4)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(np.asarray((1, 2, 3, 4)), 1)

        with pytest.raises(ValueError):
            less_than_or_equal_to(np.asarray((1, 2, 3, 4)),
                                  np.asarray((0, 1, 2, 3)))

    def test_numpyarray_passes(self):
        less_than_or_equal_to(np.asarray(((1, 2), (3, 4))), 4)
        less_than_or_equal_to(np.asarray(((1, 2), (3, 4))),
                              np.asarray(((1, 2), (3, 4))))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(np.asarray(((1, 2), (3, 4))), 1)

        with pytest.raises(ValueError):
            less_than_or_equal_to(np.asarray(((1, 2), (3, 4))),
                                  np.asarray(((0, 1), (2, 3))))


if __name__ == "__main__":
    pytest.main()
