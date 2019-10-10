import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from cdpyr.motion import pose


@pytest.fixture
def rand_vector_3d():
    return np.random.random(3)


@pytest.fixture
def rand_pos_1t():
    return np.pad(np.random.random(1), (0, 2))


@pytest.fixture
def rand_pos_2t():
    return np.pad(np.random.random(2), (0, 1))


@pytest.fixture
def rand_pos_3t():
    return np.pad(np.random.random(3), (0, 0))


@pytest.fixture
def rand_rot_1r():
    return Rotation.from_euler('z', np.random.rand()).as_dcm()


@pytest.fixture
def rand_rot_2r():
    return Rotation.from_euler('xy', np.random.random(2)).as_dcm()


@pytest.fixture
def rand_rot_3r():
    return Rotation.random().as_dcm()


@pytest.fixture
def rand_rot():
    return Rotation.random().as_dcm()


@pytest.fixture
def unit_rot():
    return Rotation.from_quat([0., 0., 0., 1.]).as_dcm()


@pytest.fixture
def empty_pose():
    return pose.Pose()


@pytest.fixture
def rand_pose_1t(rand_pos_1t, unit_rot):
    return pose.Pose(
        position=(rand_pos_1t, unit_rot)
    )


@pytest.fixture
def rand_pose_2t(rand_pos_2t, unit_rot):
    return pose.Pose(
        position=(rand_pos_2t, unit_rot)
    )


@pytest.fixture
def rand_pose_3t(rand_pos_3t, unit_rot):
    return pose.Pose(
        position=(rand_pos_3t, unit_rot)
    )


@pytest.fixture
def rand_pose_1r2t(rand_pos_2t, rand_rot_1r):
    return pose.Pose(
        position=(rand_pos_2t, rand_rot_1r)
    )


@pytest.fixture
def rand_pose_2r3t(rand_pos_3t, rand_rot_2r):
    return pose.Pose(
        position=(rand_pos_3t, rand_rot_2r)
    )


@pytest.fixture
def rand_pose_3r3t(rand_pos_3t, rand_rot_3r):
    return pose.Pose(
        position=(rand_pos_3t, rand_rot_3r)
    )


@pytest.fixture
def rand_pose_3d(rand_pos_3t, rand_rot_3r):
    return pose.Pose(
        position=(rand_pos_3t, rand_rot_3r)
    )
