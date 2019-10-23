import numpy as np
import pytest

from cdpyr.validator.numeric import nonnegative


class NonnegativeTestSuite(object):

    def test_scalar_passes(self):
        nonnegative(4)
        nonnegative(0)

    def test_scalar_fails_negative(self):
        with pytest.raises(ValueError):
            nonnegative(-4)

    def test_list_passes(self):
        nonnegative((0, 0, 0, 0))
        nonnegative((1, 2, 3, 4))

    def test_list_fails_negative(self):
        with pytest.raises(ValueError):
            nonnegative((-1, -2, -3, -4))

    def test_numpy_vector_passes(self):
        nonnegative((0, 0, 0, 0))
        nonnegative(np.asarray((1, 2, 3, 4)))

    def test_numpy_vector_fails_negative(self):
        with pytest.raises(ValueError):
            nonnegative((-1, -2, -3, -4))


if __name__ == "__main__":
    pytest.main()
