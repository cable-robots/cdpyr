import numpy as np
import pytest

from cdpyr.validator.linalg import rotation_matrix


class RotationMatrixTestSuite(object):

    def test_list_passes(self):
        rotation_matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

        rotation_matrix([
            [np.cos(np.pi / 3), -np.sin(np.pi / 3), 0],
            [np.sin(np.pi / 3), np.cos(np.pi / 3), 0],
            [0, 0, 1],
        ])

    def test_list_fails(self):
        with pytest.raises(ValueError):
            rotation_matrix([
                [1, 0, 1],
                [1, 1, 1],
                [-1, 1, 1]
            ])

        with pytest.raises(ValueError):
            rotation_matrix([
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
            ])

        with pytest.raises(ValueError):
            rotation_matrix([
                [2, 0, 0],
                [0, 2, 0],
                [0, 0, 2],
            ])

    def test_numpyarray_passes(self):
        rotation_matrix(np.asarray((
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        )))

        rotation_matrix(np.asarray((
            (np.cos(np.pi / 3), -np.sin(np.pi / 3), 0),
            (np.sin(np.pi / 3), np.cos(np.pi / 3), 0),
            (0, 0, 1)
        )))
