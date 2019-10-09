import numpy as np_
import pytest

from cdpyr import validator


class DimensionsTestSuite(object):

    def test_scalar_passes(self):
        validator.dimensions(1, 0)

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            validator.dimensions(1, 1)

    def test_list_passes(self):
        validator.dimensions((1, 2), 1)

    def test_list_fails(self):
        with pytest.raises(ValueError):
            validator.dimensions((1, 2), 2)

    def test_list_of_list_passes(self):
        validator.dimensions(((1, 2), (3, 4)), 2)

    def test_list_of_list_fails(self):
        with pytest.raises(ValueError):
            validator.dimensions(((1, 2), (3, 4)), 1)

    def test_numpyarray_passes(self):
        validator.dimensions(np_.asarray((1, 2)), 1)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            validator.dimensions(np_.asarray((1, 2)), 2)

    def test_numpyarray_passes(self):
        validator.dimensions(np_.asarray(((1, 2), (3, 4))), 2)

    def test_numpyarray_fails(self):
        with pytest.raises(ValueError):
            validator.dimensions(np_.asarray(((1, 2), (3, 4))), 1)
