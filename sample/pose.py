import numpy as np
from scipy.spatial.transform import Rotation

from cdpyr.motion import Pose


def rand_vector_3d():
    return np.random.random(3)


def rand_pos_1t():
    return np.pad(2 * (np.random.random(1) - 0.5), (0, 2))


def rand_pos_2t():
    return np.pad(2 * (np.random.random(2) - 0.5), (0, 1))


def rand_pos_3t():
    return np.pad(2 * (np.random.random(3) - 0.5), (0, 0))


def rand_rot_1r():
    return Rotation.from_euler('z',
                               (2 * np.pi * (np.random.rand() - 0.5))
                               ).as_dcm()


def rand_rot_2r():
    return Rotation.from_euler('yx',
                               (2 * np.pi * (np.random.random(2) - 0.5))
                               ).as_dcm()


def rand_rot_3r():
    return Rotation.random().as_dcm()


def rand_rot():
    return Rotation.random().as_dcm()


def unit_rot():
    return Rotation.from_quat([0., 0., 0., 1.]).as_dcm()


def empty_pose():
    return Pose()


def rand_pose_1t():
    return Pose((rand_pos_1t(), unit_rot()))


def rand_pose_2t():
    return Pose((rand_pos_2t(), unit_rot()))


def rand_pose_3t():
    return Pose((rand_pos_3t(), unit_rot()))


def rand_pose_1r2t():
    return Pose((rand_pos_2t(), rand_rot_1r()))


def rand_pose_2r3t():
    return Pose((rand_pos_3t(), rand_rot_2r()))


def rand_pose_3r3t():
    return Pose((rand_pos_3t(), rand_rot_3r()))


def rand_pose_3d():
    return Pose((rand_pos_3t(), rand_rot_3r()))
