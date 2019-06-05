from unittest import TestCase

import numpy as np
from scipy.spatial.transform import Rotation

from cdpyr.motion import Pose


class TestPose(TestCase):
    rotation: Rotation
    position: np.ndarray
    time: float

    def setUp(self):
        self.rotation = Rotation.random(num=1)[0]
        self.position = np.random.rand(3)
        self.time = np.random.rand(1)[0]

    def test_position_is_initialized_correctly(self):
        pose = Pose(position=self.position, time=self.time)

        np.testing.assert_allclose(pose.position, self.position)
        np.testing.assert_allclose(pose.dcm, np.eye(3))
        np.testing.assert_allclose(pose.time, self.time)

    def test_orientation_is_initialized_correctly_by_dcm(self):
        pose = Pose(dcm=self.rotation.as_dcm(), time=self.time,
                    position=self.position)

        np.testing.assert_allclose(pose.dcm, self.rotation.as_dcm())
        np.testing.assert_allclose(pose.position, self.position)
        np.testing.assert_allclose(pose.time, self.time)

    def test_orientation_is_initialized_correctly_by_quaternion(self):
        pose = Pose(quaternion=self.rotation.as_quat(), time=self.time,
                    position=self.position)

        np.testing.assert_allclose(pose.quaternion, self.rotation.as_quat())
        np.testing.assert_allclose(pose.dcm, self.rotation.as_dcm())
        np.testing.assert_allclose(pose.position, self.position)
        np.testing.assert_allclose(pose.time, self.time)

    def test_orientation_is_initialized_correctly_by_rotation(self):
        pose = Pose(orientation=self.rotation, time=self.time,
                    position=self.position)

        np.testing.assert_allclose(pose.quaternion, self.rotation.as_quat())
        np.testing.assert_allclose(pose.dcm, self.rotation.as_dcm())
        np.testing.assert_allclose(pose.position, self.position)
        np.testing.assert_allclose(pose.time, self.time)

    def test_pose_to_str(self):
        pose = Pose(position=self.position, dcm=self.rotation.as_dcm(), time=self.time)

        expected = np.array2string(np.hstack([self.time, self.position,
                                              self.rotation.as_dcm().reshape(9)]),
                                   separator=',',
                                   formatter={'float_kind': lambda x: "%.2f" %
                                                                      x})[1:-1]
        np.testing.assert_allclose(pose.position, self.position)
        np.testing.assert_allclose(pose.dcm, self.rotation.as_dcm())
        np.testing.assert_allclose(pose.time, self.time)
        self.assertEqual(expected, str(pose))

    def test_compare_two_poses_lt(self):
        p0 = Pose(time=0)
        p1 = Pose(time=1)

        self.assertTrue(p0 < p1)
        self.assertFalse(p1 < p0)
        self.assertLess(p0, p1)

    def test_compare_two_poses_gt(self):
        p0 = Pose(time=0)
        p1 = Pose(time=1)

        self.assertFalse(p0 > p1)
        self.assertTrue(p1 > p0)
        self.assertGreater(p1, p0)

    def test_compare_two_poses_le(self):
        p0 = Pose(time=0)
        p1 = Pose(time=1)

        self.assertTrue(p0 <= p1)
        self.assertFalse(p1 <= p0)
        self.assertLess(p0, p1)

    def test_compare_two_poses_ge(self):
        p0 = Pose(time=0)
        p1 = Pose(time=1)

        self.assertFalse(p0 >= p1)
        self.assertTrue(p1 >= p0)
        self.assertGreater(p1, p0)
