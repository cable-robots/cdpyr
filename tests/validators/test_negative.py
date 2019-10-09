import numpy as np_
import pytest

from cdpyr import validator


class NegativeTestSuite(object):

    def test_scalar_passes(self):
        validator.negative(-4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            validator.negative(4)
        with pytest.raises(ValueError):
            validator.negative(0)

    def test_list_passes(self):
        validator.negative([-1, -2, -3, -4])

    def test_tuple_passes(self):
        validator.negative((-1, -2, -3, -4))

    def test_list_fails(self):
        with pytest.raises(ValueError):
            validator.negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            validator.negative((1, 2, 3, 4))

    def test_tuple_fails(self):
        with pytest.raises(ValueError):
            validator.negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            validator.negative((1, 2, 3, 4))

    def test_numpy_vector_passes(self):
        validator.negative(np_.asarray((-1, -2, -3, -4)))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            validator.negative((0, 0, 0, 0))

        with pytest.raises(ValueError):
            validator.negative((1, 2, 3, 4))
