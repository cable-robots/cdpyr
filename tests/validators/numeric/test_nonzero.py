import numpy as np
import pytest

from cdpyr.validator.numeric import nonzero


class NonzeroTestSuite(object):

    def test_scalar_passes(self):
        nonzero(4)
        nonzero(-4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            nonzero(0)

    def test_list_passes(self):
        nonzero([4] * 4)
        nonzero([-4] * 4)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            nonzero([0] * 4)

    def test_numpy_vector_passes(self):
        nonzero(np.asarray([4] * 4))
        nonzero(np.asarray([-4] * 4))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            nonzero([0] * 4)
