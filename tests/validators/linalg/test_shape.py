from __future__ import annotations

import pytest

from cdpyr.validator.linalg import shape

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class ShapeTestSuite(object):

    def test_scalar_passes(self):
        shape(1, ())

    def test_scalar_fails(self):
        with pytest.raises(ValueError):
            shape(1, 1)
        with pytest.raises(ValueError):
            shape([1, 2], 2)
        with pytest.raises(ValueError):
            shape(1, (1,))

    def test_list_passes(self):
        shape([1], (1,))
        shape([1, 2, 3], (3,))
        shape([[1, 2], [3, 4]], (2, 2))

    def test_list_fails(self):
        with pytest.raises(ValueError):
            shape([1, 2, 3], (2,))
        with pytest.raises(ValueError):
            shape([1, 2, 3], (1, 1))

    def test_tuple_passes(self):
        shape((1), ())
        shape((1, 2, 3), (3,))
        shape(((1, 2), (3, 4)), (2, 2))

    def test_tuple_fails(self):
        with pytest.raises(ValueError):
            shape((1, 2, 3), (2,))
        with pytest.raises(ValueError):
            shape((1, 2, 3), (1, 1))


if __name__ == "__main__":
    pytest.main()
