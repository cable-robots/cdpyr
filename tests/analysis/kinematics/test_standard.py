from typing import Sequence

import numpy as np
import pytest

from cdpyr.typing import Matrix, Num, Vector


class StandardKinematicsTestSuite(object):

    def test_motionpattern_1t(self, robot_1t, rand_pose_1t, ik_standard):
        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_1t, rand_pose_1t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_1t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_1t.num_kinematic_chains)
        assert unit_directions[1:, :] == pytest.approx(
            np.zeros((2, robot_1t.num_kinematic_chains)))
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_1t.num_kinematic_chains, ))

    def test_motionpattern_2t(self, robot_2t, rand_pose_2t, ik_standard):
        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_2t, rand_pose_2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_2t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_2t.num_kinematic_chains)
        assert unit_directions[2:, :] == pytest.approx(
            np.zeros((1, robot_2t.num_kinematic_chains)))
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_2t.num_kinematic_chains, ))

    def test_motionpattern_3t(self, robot_3t, rand_pose_3t, ik_standard):
        length: Sequence[Num]
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_3t, rand_pose_3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_3t.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_3t.num_kinematic_chains, ))

    def test_motionpattern_1r2t(self, robot_1r2t, rand_pose_1r2t, ik_standard):
        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_1r2t,
                                                       rand_pose_1r2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_1r2t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_1r2t.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_1r2t.num_kinematic_chains, ))

    def test_motionpattern_2r3t(self, robot_2r3t, rand_pose_2r3t, ik_standard):
        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_2r3t,
                                                       rand_pose_2r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_2r3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_2r3t.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_2r3t.num_kinematic_chains, ))

    def test_motionpattern_3r3t(self, robot_3r3t, rand_pose_3r3t, ik_standard):
        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot_3r3t,
                                                       rand_pose_3r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_3r3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot_3r3t.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(
            np.ones(robot_3r3t.num_kinematic_chains, ))
