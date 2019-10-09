import numpy as np_
import pytest

from cdpyr.validator import less_than_or_equal_to


class LessThanOrEqualToTestSuite(object):

    def test_scalar_passes(self):
        less_than_or_equal_to(0, 0)
        less_than_or_equal_to(1, 1)
        less_than_or_equal_to(-1, -1)

    def test_list_passes(self):
        less_than_or_equal_to([1, 2, 3, 4], 4)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to([1, 2, 3, 4], 1)

    def test_list_of_list_passes(self):
        less_than_or_equal_to(((1, 2), (3, 4)), 4)

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(((1, 2), (3, 4)), 1)

    def test_numpyarray_passes(self):
        less_than_or_equal_to(np_.asarray((1, 2, 3, 4)), 4)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(np_.asarray((1, 2, 3, 4)), 1)

    def test_numpyarray_passes(self):
        less_than_or_equal_to(np_.asarray(((1, 2), (3, 4))), 4)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than_or_equal_to(np_.asarray(((1, 2), (3, 4))), 1)
