import numpy as np
import pytest

from cdpyr.validator.numeric import nonpositive


class NonpositiveTestSuite(object):

    def test_scalar_passes(self):
        nonpositive(-4)
        nonpositive(0)

    def test_scalar_fails_negative(self):
        with pytest.raises(ValueError):
            nonpositive(4)

    def test_list_passes(self):
        nonpositive((0, 0, 0, 0))
        nonpositive((-1, -2, -3, -4))

    def test_list_fails_negative(self):
        with pytest.raises(ValueError):
            nonpositive((1, 2, 3, 4))

    def test_numpy_vector_passes(self):
        nonpositive((0, 0, 0, 0))
        nonpositive(np.asarray((-1, -2, -3, -4)))

    def test_numpy_vector_fails_negative(self):
        with pytest.raises(ValueError):
            nonpositive((1, 2, 3, 4))
