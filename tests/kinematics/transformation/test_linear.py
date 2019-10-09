from typing import Sequence

import numpy as np
from pytest import approx, mark

import cdpyr


class LinearTransformationTestSuite(object):

    def test_empty_object(self):
        linear = cdpyr.kinematics.transformation.Linear()

        assert isinstance(linear, cdpyr.kinematics.transformation.Linear)

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "pos",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_position_from_list_as_positional_argument(self,
                                                            pos: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            pos
        )

        expected = np.asarray(pos
                              if isinstance(pos, Sequence)
                              else [pos]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx(expected)
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "pos",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_position_from_list_as_keyword_argument(self, pos: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            position=pos,
        )

        expected = np.asarray(pos
                              if isinstance(pos, Sequence)
                              else [pos]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx(expected)
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "pos",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_position_from_numpyarray_as_positional_argument(self,
                                                                  pos:
                                                                  np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            pos
        )

        expected = np.asarray(pos if isinstance(pos, np.ndarray) else [pos])

        assert linear.position.shape == (3,)
        assert linear.position == approx(expected)
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "pos",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_position_from_numpyarray_as_keyword_argument(self,
                                                               pos: np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            position=pos,
        )

        expected = np.asarray(pos if isinstance(pos, np.ndarray) else [pos])

        assert linear.position.shape == (3,)
        assert linear.position == approx(expected)
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_list_as_positional_argument(self,
                                                            vel: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            None,
            vel
        )

        expected = np.asarray(vel
                              if isinstance(vel, Sequence)
                              else [vel]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx(expected)
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_list_as_keyword_argument(self, vel: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            velocity=vel,
        )

        expected = np.asarray(vel
                              if isinstance(vel, Sequence)
                              else [vel]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx(expected)
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_numpyarray_as_positional_argument(self,
                                                                  vel:
                                                                  np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            None,
            vel
        )

        expected = np.asarray(vel if isinstance(vel, np.ndarray) else [vel])

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx(expected)
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_numpyarray_as_keyword_argument(self,
                                                               vel: np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            velocity=vel,
        )

        expected = np.asarray(vel if isinstance(vel, np.ndarray) else [vel])

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx(expected)
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "acc",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_list_as_positional_argument(self,
                                                                acc: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            None,
            None,
            acc
        )

        expected = np.asarray(acc
                              if isinstance(acc, Sequence)
                              else [acc]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx(expected)

    @mark.parametrize(
        "acc",
        [
            (np.zeros((3,)).tolist()),  # 3x1 zeros
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_list_as_keyword_argument(self,
                                                             acc: Sequence):
        linear = cdpyr.kinematics.transformation.Linear(
            acceleration=acc
        )

        expected = np.asarray(acc
                              if isinstance(acc, Sequence)
                              else [acc]
                              )

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx(expected)

    @mark.parametrize(
        "acc",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_numpyarray_as_positional_argument(self,
                                                                      acc:
                                                                      np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            None,
            None,
            acc
        )

        expected = np.asarray(acc if isinstance(acc, np.ndarray) else [acc])

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx(expected)

    @mark.parametrize(
        "acc",
        [
            (np.zeros((3,))),  # 3x1 zeros
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_numpyarray_as_keyword_argument(self,
                                                                   acc:
                                                                   np.ndarray):
        linear = cdpyr.kinematics.transformation.Linear(
            acceleration=acc,
        )

        expected = np.asarray(acc if isinstance(acc, np.ndarray) else [acc])

        assert linear.position.shape == (3,)
        assert linear.position == approx([0., 0., 0.])
        assert linear.velocity.shape == (3,)
        assert linear.velocity == approx([0., 0., 0.])
        assert linear.acceleration.shape == (3,)
        assert linear.acceleration == approx(expected)
