from __future__ import annotations

import itertools

import numpy as np
import pytest

from cdpyr.kinematics.transformation import Linear
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class LinearTransformationTestSuite(object):

    @pytest.mark.parametrize(
            ('pos', 'vel', 'acc'),
            (
                    itertools.product(
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                    )
            )
    )
    def test_init(self, pos: Matrix, vel: Matrix, acc: Matrix):
        linear = Linear(pos, vel, acc)

        pos = np.asarray(pos if pos is not None else [0.0, 0.0, 0.0])
        vel = np.asarray(vel if vel is not None else [0.0, 0.0, 0.0])
        acc = np.asarray(acc if acc is not None else [0.0, 0.0, 0.0])

        assert linear.position.shape == pos.shape
        assert linear.velocity.shape == vel.shape
        assert linear.acceleration.shape == acc.shape
        assert linear.position == pytest.approx(pos)
        assert linear.velocity == pytest.approx(vel)
        assert linear.acceleration == pytest.approx(acc)

    @pytest.mark.parametrize(
            ('pos', 'coordinate'),
            (
                    itertools.product(
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (np.zeros((3,)), np.random.random((3,)),
                             np.random.random((3, 5))),
                    )
            )
    )
    def test_apply_transformation(self, pos: Vector, coordinate: Matrix):
        linear = Linear(pos)

        pos = np.asarray(pos if pos is not None else [0.0, 0.0, 0.0])

        single_coordinate = coordinate.ndim == 1
        if single_coordinate:
            expected_transformed = pos + coordinate
        else:
            expected_transformed = pos[:, None] + coordinate

        transformed = linear.apply(coordinate)

        assert transformed.shape == expected_transformed.shape
        assert transformed == pytest.approx(expected_transformed)


if __name__ == "__main__":
    pytest.main()
