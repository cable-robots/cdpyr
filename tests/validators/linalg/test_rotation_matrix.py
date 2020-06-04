from __future__ import annotations

import numpy as np
import pytest

from cdpyr.validator.linalg import rotation_matrix

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


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

    def test_rand_rot_1r(self, rand_rot_1r):
        rotation_matrix(rand_rot_1r, 'rand_rot_1r')

    def test_rand_rot_2r(self, rand_rot_2r):
        rotation_matrix(rand_rot_2r, 'rand_rot_2r')

    def test_rand_rot_3r(self, rand_rot_3r):
        rotation_matrix(rand_rot_3r, 'rand_rot_3r')


if __name__ == "__main__":
    pytest.main()
