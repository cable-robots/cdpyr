from typing import Sequence

import numpy as np
import pytest
import cdpyr
from cdpyr.typing import Matrix, Num, Vector
from sample import robots


class StandardKinematicsTestSuite(object):

    def test_motionpattern_1t(self, rand_pose_1t, ik_standard):
        robot = robots.robot_1t()

        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_1t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert unit_directions[1:,:] == pytest.approx(np.zeros((2, robot.num_kinematic_chains)))
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))

    def test_motionpattern_2t(self, rand_pose_2t, ik_standard):
        robot = robots.robot_2t()

        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert unit_directions[2:,:] == pytest.approx(np.zeros((1, robot.num_kinematic_chains)))
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))

    def test_motionpattern_3t(self, rand_pose_3t, ik_standard):
        robot = robots.robot_3t()

        length: Sequence[Num]
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))

    def test_motionpattern_1r2t(self, rand_pose_1r2t, ik_standard):
        robot = robots.robot_1r2t()

        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_1r2t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))

    def test_motionpattern_2r3t(self, rand_pose_2r3t, ik_standard):
        robot = robots.robot_2r3t()

        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_2r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))

    def test_motionpattern_3r3t(self, rand_pose_3r3t, ik_standard):
        robot = robots.robot_3r3t()

        length: Vector
        unit_directions: Matrix
        length, unit_directions = ik_standard.backward(robot, rand_pose_3r3t)

        # TODO implement the test for `forward`, too

        assert length.ndim == 1
        assert length.shape == (robot.num_kinematic_chains,)
        assert (length >= 0).all()
        assert unit_directions.shape == (3, robot.num_kinematic_chains)
        assert np.linalg.norm(unit_directions, axis=0) == pytest.approx(np.ones(robot.num_kinematic_chains, ))
