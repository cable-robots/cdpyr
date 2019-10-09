import numpy as np_
import pytest

from cdpyr import validator


class NonpositiveTestSuite(object):

    def test_scalar_passes(self):
        validator.nonpositive(-4)
        validator.nonpositive(0)

    def test_scalar_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonpositive(4)

    def test_list_passes(self):
        validator.nonpositive((0, 0, 0, 0))
        validator.nonpositive((-1, -2, -3, -4))

    def test_list_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonpositive((1, 2, 3, 4))

    def test_numpy_vector_passes(self):
        validator.nonpositive((0, 0, 0, 0))
        validator.nonpositive(np_.asarray((-1, -2, -3, -4)))

    def test_numpy_vector_fails_negative(self):
        with pytest.raises(ValueError) as excinfo:
            validator.nonpositive((1, 2, 3, 4))
