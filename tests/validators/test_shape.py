import pytest

from cdpyr import validator


class ShapeTestSuite(object):

    def test_scalar_passes(self):
        validator.shape(1, ())

    def test_scalar_fails(self):
        with pytest.raises(ValueError) as excinfo:
            validator.shape(1, 1)
        with pytest.raises(ValueError) as excinfo:
            validator.shape([1, 2], 2)
        with pytest.raises(ValueError) as excinfo:
            validator.shape(1, (1,))

    def test_list_passes(self):
        validator.shape([1], (1,))
        validator.shape([1, 2, 3], (3,))
        validator.shape([[1, 2], [3, 4]], (2,2))

    def test_list_fails(self):
        with pytest.raises(ValueError) as excinfo:
            validator.shape([1, 2, 3], (2,))
        with pytest.raises(ValueError) as excinfo:
            validator.shape([1, 2, 3], (1, 1))

    def test_tuple_passes(self):
        validator.shape((1), ())
        validator.shape((1, 2, 3), (3,))
        validator.shape(((1, 2), (3, 4)), (2,2))

    def test_tuple_fails(self):
        with pytest.raises(ValueError) as excinfo:
            validator.shape((1, 2, 3), (2,))
        with pytest.raises(ValueError) as excinfo:
            validator.shape((1, 2, 3), (1, 1))
