import numpy as np
import pytest

from cdpyr.validator.numeric import nonnan


class NonnanTestSuite(object):

    def test_scalar_pass(self):
        nonnan(4)
        nonnan(-4)

    def test_scalar_failses(self):
        with pytest.raises(ValueError):
            nonnan(np.nan)

        with pytest.raises(ValueError):
            nonnan(-np.nan)

    def test_list_passes(self):
        nonnan([1, 2, 3, 4])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            nonnan([np.nan, np.nan, np.nan, np.nan])

        with pytest.raises(ValueError):
            nonnan([np.nan, -np.nan, np.nan, -np.nan])

    def test_numpyarray_passes(self):
        nonnan(np.asarray((1, 2, 3, 4)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            nonnan(np.asarray((np.nan, np.nan, np.nan, np.nan)))

        with pytest.raises(ValueError):
            nonnan(np.asarray((-np.nan, np.nan, -np.nan, np.nan)))
