import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from cdpyr.motion import pose


@pytest.fixture
def empty_pose():
    return pose.Pose()


@pytest.fixture
def random_pose_3d():
    return pose.Pose(
        position=[
            np.random.random(3),
            Rotation.random().as_dcm()
        ]
    )
