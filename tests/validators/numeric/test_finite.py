import numpy as np
import pytest

from cdpyr.validator.numeric import finite


class FiniteTestSuite(object):

    def test_scalar_pass(self):
        finite(4)
        finite(-4)

    def test_scalar_failses(self):
        with pytest.raises(ValueError):
            finite(np.inf)

        with pytest.raises(ValueError):
            finite(-np.inf)

    def test_list_passes(self):
        finite([1, 2, 3, 4])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            finite([np.inf, np.inf, np.inf, np.inf])

        with pytest.raises(ValueError):
            finite([np.inf, -np.inf, np.inf, -np.inf])

    def test_numpyarray_passes(self):
        finite(np.asarray((1, 2, 3, 4)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            finite(np.asarray((np.inf, np.inf, np.inf, np.inf)))

        with pytest.raises(ValueError):
            finite(np.asarray((-np.inf, np.inf, -np.inf, np.inf)))
