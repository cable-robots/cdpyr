import numpy as np
import pytest

from cdpyr.validator.linalg import unit_vector


class UnitVectorTestSuite(object):

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            unit_vector(1)

        with pytest.raises(ValueError):
            unit_vector(0.3)

    def test_list_passes(self):
        unit_vector([1, 0, 0])
        unit_vector((1 / np.sqrt(2) * np.asarray((1, -1, 0))).tolist())

    def test_list_fails(self):
        with pytest.raises(ValueError):
            unit_vector([1, 1, 0])

    def test_numpyarray_passes(self):
        unit_vector(np.asarray((1, 0, 0)))
        unit_vector(1 / np.sqrt(2) * np.asarray((1, -1, 0)))

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            unit_vector(np.asarray((1, 1, 0)))
