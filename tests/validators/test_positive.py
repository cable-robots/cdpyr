import numpy as np_
import pytest

from cdpyr import validator


class PositiveTestSuite(object):

    def test_scalar_passes(self):
        validator.positive(4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            validator.positive(-4)
        with pytest.raises(ValueError):
            validator.positive(0)

    def test_list_passes(self):
        validator.positive((1, 2, 3, 4))

    def test_list_fails(self):
        with pytest.raises(ValueError):
            validator.positive([0, 0, 0, 0])

        with pytest.raises(ValueError):
            validator.positive([-1, -2, -3, -4])

    def test_tuple_passes(self):
        validator.positive((1, 2, 3, 4))

    def test_tuple_fails(self):
        with pytest.raises(ValueError):
            validator.positive((0, 0, 0, 0))

        with pytest.raises(ValueError):
            validator.positive((-1, -2, -3, -4))

    def test_numpy_vector_passes(self):
        validator.positive(np_.asarray((1, 2, 3, 4)))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            validator.positive((0, 0, 0, 0))

        with pytest.raises(ValueError):
            validator.positive((-1, -2, -3, -4))
