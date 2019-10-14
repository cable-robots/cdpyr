import numpy as np
import pytest

from cdpyr.validator.numeric import negative


class NegativeTestSuite(object):

    def test_scalar_passes(self):
        negative(-4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            negative(4)
        with pytest.raises(ValueError):
            negative(0)

    def test_list_passes(self):
        negative([-1, -2, -3, -4])

    def test_tuple_passes(self):
        negative((-1, -2, -3, -4))

    def test_list_fails(self):
        with pytest.raises(ValueError):
            negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            negative((1, 2, 3, 4))

    def test_tuple_fails(self):
        with pytest.raises(ValueError):
            negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            negative((1, 2, 3, 4))

    def test_numpy_vector_passes(self):
        negative(np.asarray((-1, -2, -3, -4)))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            negative((1, 2, 3, 4))
