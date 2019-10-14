import numpy as np
import pytest

from cdpyr.validator import equal_to


class EqualToTestSuite(object):

    def test_scalar_passes(self):
        equal_to(1, 1)
        equal_to(0, 0)
        equal_to(-1, -1)

    def test_list_passes(self):
        equal_to([1, 1, 1, 1], 1)
        equal_to([1, 1, 1, 1], [1, 1, 1, 1])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            equal_to([1, 1, 1, 1], 0)

        with pytest.raises(ValueError):
            equal_to([1, 1, 1, 1], [0, 0, 0, 0])

    def test_list_of_list_passes(self):
        equal_to(((1, 1), (1, 1)), 1)
        equal_to(((1, 1), (1, 1)), ((1, 1), (1, 1)))

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            equal_to(((1, 1), (1, 1)), 0)
        with pytest.raises(ValueError):
            equal_to(((1, 1), (1, 1)), ((0, 0), (0, 0)))

    def test_numpyarray_passes(self):
        equal_to(np.asarray((1, 1, 1, 1)), 1)
        equal_to(np.asarray((1, 1, 1, 1)), np.asarray((1, 1, 1, 1)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            equal_to(np.asarray((1, 1, 1, 1)), 0)

        with pytest.raises(ValueError):
            equal_to(np.asarray((1, 1, 1, 1)), np.asarray((0, 0, 0, 0)))

    def test_numpyarray_passes(self):
        equal_to(np.asarray(((1, 1), (1, 1))), 1)
        equal_to(np.asarray(((1, 1), (1, 1))), np.asarray(((1, 1), (1, 1))))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            equal_to(np.asarray(((1, 1), (1, 1))), 0)

        with pytest.raises(ValueError):
            equal_to(np.asarray(((1, 1), (1, 1))), np.asarray(((0, 0), (0, 0))))
