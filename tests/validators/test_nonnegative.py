import numpy as np_
import pytest

from cdpyr import validator


class NonnegativeTestSuite(object):

    def test_scalar_passes(self):
        validator.nonnegative(4)
        validator.nonnegative(0)

    def test_scalar_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonnegative(-4)

    def test_list_passes(self):
        validator.nonnegative((0, 0, 0, 0))
        validator.nonnegative((1, 2, 3, 4))

    def test_list_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonnegative((-1, -2, -3, -4))

    def test_numpy_vector_passes(self):
        validator.nonnegative((0, 0, 0, 0))
        validator.nonnegative(np_.asarray((1, 2, 3, 4)))

    def test_numpy_vector_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonnegative((-1, -2, -3, -4))
