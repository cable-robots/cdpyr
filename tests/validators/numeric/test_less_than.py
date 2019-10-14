import numpy as np
import pytest

from cdpyr.validator.numeric import less_than


class LessThanTestSuite(object):

    def test_scalar_passes(self):
        less_than(0, 1)
        less_than(-1, 0)

    def test_list_passes(self):
        less_than([1, 2, 3, 4], 5)
        less_than([1, 2, 3, 4], [2, 3, 4, 5])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            less_than([1, 2, 3, 4], 0)

        with pytest.raises(ValueError):
            less_than([1, 2, 3, 4], [1, 2, 3, 4])

    def test_list_of_list_passes(self):
        less_than(((1, 2), (3, 4)), 5)
        less_than(((1, 2), (3, 4)), ((2, 3), (4, 5)))

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            less_than(((1, 2), (3, 4)), 0)
        with pytest.raises(ValueError):
            less_than(((1, 2), (3, 4)), ((1, 2), (3, 4)))

    def test_numpyarray_passes(self):
        less_than(np.asarray((1, 2, 3, 4)), 5)
        less_than(np.asarray((1, 2, 3, 4)), np.asarray((2, 3, 4, 5)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than(np.asarray((1, 2, 3, 4)), 0)
        with pytest.raises(ValueError):
            less_than(np.asarray((1, 2, 3, 4)), np.asarray((1, 2, 3, 4)))

    def test_numpyarray_passes(self):
        less_than(np.asarray(((1, 2), (3, 4))), 5)
        less_than(np.asarray(((1, 2), (3, 4))), np.asarray(((2, 3), (4, 5))))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            less_than(np.asarray(((1, 2), (3, 4))), 0)

        with pytest.raises(ValueError):
            less_than(np.asarray(((1, 2), (3, 4))), np.asarray(((1, 2), (3, 4))))
