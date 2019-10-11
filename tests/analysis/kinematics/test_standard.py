from typing import Sequence

import numpy as np
import pytest

from cdpyr.typing import Matrix, Num, Vector


class StandardKinematicsTestSuite(object):

    def test_motionpattern_1t(self, robot_1t, rand_pose_1t, ik_standard):
        length: Vector
        directions: Matrix
        length, directions = ik_standard.backward(robot_1t, rand_pose_1t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_1t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (1, robot_1t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_1t.num_kinematic_chains, ))
        assert rand_pose_1t.linear.position[0:1, np.newaxis] \
               + length * directions == pytest.approx(robot_1t.ai[0:1, :])

    def test_motionpattern_2t(self, robot_2t, rand_pose_2t, ik_standard):
        length: Vector
        directions: Matrix
        length, directions = ik_standard.backward(robot_2t, rand_pose_2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_2t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (2, robot_2t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_2t.num_kinematic_chains, ))
        assert rand_pose_2t.linear.position[0:2, np.newaxis] \
               + length * directions == pytest.approx(robot_2t.ai[0:2, :])

    def test_motionpattern_3t(self, robot_3t, rand_pose_3t, ik_standard):
        length: Sequence[Num]
        directions: Matrix
        length, directions = ik_standard.backward(robot_3t, rand_pose_3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (3, robot_3t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_3t.num_kinematic_chains, ))
        assert rand_pose_3t.linear.position[0:3, np.newaxis] \
               + length * directions == pytest.approx(robot_3t.ai[0:3, :])

    def test_motionpattern_1r2t(self, robot_1r2t, rand_pose_1r2t, ik_standard):
        length: Vector
        directions: Matrix
        length, directions = ik_standard.backward(robot_1r2t, rand_pose_1r2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_1r2t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (2, robot_1r2t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_1r2t.num_kinematic_chains, ))
        assert rand_pose_1r2t.linear.position[0:2, np.newaxis] \
               + rand_pose_1r2t.angular.dcm[0:2, 0:2].dot(
            robot_1r2t.platforms[0].bi[0:2, :]) \
               + length * directions == pytest.approx(robot_1r2t.ai[0:2, :])

    def test_motionpattern_2r3t(self, robot_2r3t, rand_pose_2r3t, ik_standard):
        length: Vector
        directions: Matrix
        length, directions = ik_standard.backward(robot_2r3t, rand_pose_2r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_2r3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (3, robot_2r3t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_2r3t.num_kinematic_chains, ))
        assert rand_pose_2r3t.linear.position[:, np.newaxis] \
               + rand_pose_2r3t.angular.dcm.dot(robot_2r3t.platforms[0].bi) \
               + length * directions == pytest.approx(robot_2r3t.ai)

    def test_motionpattern_3r3t(self, robot_3r3t, rand_pose_3r3t, ik_standard):
        length: Vector
        directions: Matrix
        length, directions = ik_standard.backward(robot_3r3t, rand_pose_3r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot_3r3t.num_kinematic_chains,)
        assert (length >= 0).all()
        assert directions.shape == (3, robot_3r3t.num_kinematic_chains)
        assert np.linalg.norm(directions, axis=0) == pytest.approx(
            np.ones(robot_3r3t.num_kinematic_chains, ))
        assert rand_pose_3r3t.linear.position[:, np.newaxis] \
               + rand_pose_3r3t.angular.dcm.dot(robot_3r3t.platforms[0].bi) \
               + length * directions == pytest.approx(robot_3r3t.ai)
