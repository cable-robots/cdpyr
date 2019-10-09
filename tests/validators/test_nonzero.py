import numpy as np_
import pytest

from cdpyr import validator


class NonzeroTestSuite(object):

    def test_scalar_passes(self):
        validator.nonzero(4)
        validator.nonzero(-4)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            validator.nonzero(0)

    def test_list_passes(self):
        validator.nonzero([4] * 4)
        validator.nonzero([-4] * 4)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            validator.nonzero([0] * 4)

    def test_numpy_vector_passes(self):
        validator.nonzero(np_.asarray([4] * 4))
        validator.nonzero(np_.asarray([-4] * 4))

    def test_numpy_vector_fails(self):
        with pytest.raises(ValueError):
            validator.nonzero([0] * 4)
