import numpy as np
import pytest

import cdpyr
from cdpyr.data import robots

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

robot_1t = pytest.fixture(robots.robot_1t, name='robot_1t')
robot_2t = pytest.fixture(robots.robot_2t, name='robot_2t')
robot_3t = pytest.fixture(robots.robot_3t, name='robot_3t')
robot_1r2t = pytest.fixture(robots.robot_1r2t, name='robot_1r2t')
robot_2r3t = pytest.fixture(robots.robot_2r3t, name='robot_2r3t')
robot_3r3t = pytest.fixture(robots.robot_3r3t, name='robot_3r3t')
ipanema_3 = pytest.fixture(robots.ipanema_3, name='ipanema_3')


@pytest.fixture
def rand_vector_3d():
    return np.random.random(3)


@pytest.fixture
def rand_pos_1t():
    return np.pad(2 * (np.random.random(1) - 0.5), (0, 2))


@pytest.fixture
def rand_pos_2t():
    return np.pad(2 * (np.random.random(2) - 0.5), (0, 1))


@pytest.fixture
def rand_pos_3t():
    return np.pad(2 * (np.random.random(3) - 0.5), (0, 0))


@pytest.fixture
def rand_rot_1r():
    return cdpyr.kinematics.transformation.Angular(sequence='z', euler=np.pi * (
            np.random.random() - 0.5)).dcm


@pytest.fixture
def rand_rot_2r():
    return cdpyr.kinematics.transformation.Angular(sequence='xy',
                                                   euler=np.pi * (
                                                           np.random.random(
                                                                   2) -
                                                           0.5)).dcm


@pytest.fixture
def rand_rot_3r():
    return cdpyr.kinematics.transformation.Angular.random().dcm


@pytest.fixture
def rand_rot():
    return cdpyr.kinematics.transformation.Angular.random().dcm


@pytest.fixture
def unit_rot():
    return cdpyr.kinematics.transformation.Angular().dcm


@pytest.fixture
def empty_pose():
    return cdpyr.motion.pose.Pose()


@pytest.fixture
def rand_pose_1t(rand_pos_1t, unit_rot):
    return cdpyr.motion.pose.Pose(rand_pos_1t, unit_rot)


@pytest.fixture
def rand_pose_2t(rand_pos_2t, unit_rot):
    return cdpyr.motion.pose.Pose(rand_pos_2t, unit_rot)


@pytest.fixture
def rand_pose_3t(rand_pos_3t, unit_rot):
    return cdpyr.motion.pose.Pose(rand_pos_3t, unit_rot)


@pytest.fixture
def rand_pose_1r2t(rand_pos_2t, rand_rot_1r):
    return cdpyr.motion.pose.Pose(rand_pos_2t, rand_rot_1r)


@pytest.fixture
def rand_pose_2r3t(rand_pos_3t, rand_rot_2r):
    return cdpyr.motion.pose.Pose(rand_pos_3t, rand_rot_2r)


@pytest.fixture
def rand_pose_3r3t(rand_pos_3t, rand_rot_3r):
    return cdpyr.motion.pose.Pose(rand_pos_3t, rand_rot_3r)


@pytest.fixture
def rand_pose_3d(rand_pos_3t, rand_rot_3r):
    return cdpyr.motion.pose.Pose(rand_pos_3t, rand_rot_3r)


ik_standard = pytest.fixture(lambda: cdpyr.analysis.kinematics.Standard(),
                             name='ik_standard')
ik_pulley = pytest.fixture(lambda: cdpyr.analysis.kinematics.Pulley(),
                           name='ik_pulley')
