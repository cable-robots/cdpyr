import numpy as np
import pytest

from cdpyr.validator import greater_than


class GreaterThanTestSuite(object):

    def test_scalar_passes(self):
        greater_than(1, 0)
        greater_than(0, -1)

    def test_list_passes(self):
        greater_than([1, 2, 3, 4], 0)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            greater_than([1, 2, 3, 4], 5)

    def test_list_of_list_passes(self):
        greater_than(((1, 2), (3, 4)), 0)

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            greater_than(((1, 2), (3, 4)), 5)

    def test_numpyarray_passes(self):
        greater_than(np.asarray((1, 2, 3, 4)), 0)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            greater_than(np.asarray((1, 2, 3, 4)), 5)

    def test_numpyarray_passes(self):
        greater_than(np.asarray(((1, 2), (3, 4))), 0)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            greater_than(np.asarray(((1, 2), (3, 4))), 5)
