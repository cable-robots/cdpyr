from unittest import TestCase

import numpy as np
import quaternion

from cdpyr.motion import Pose


class TestPose(TestCase):
    def test_position_is_initialized_correctly(self):
        p = np.random.rand(3)
        pose = Pose(position=p)

        np.testing.assert_array_almost_equal(p, pose.position)
        np.testing.assert_almost_equal(np.eye(3), pose.rotation_matrix)
        np.testing.assert_almost_equal(np.eye(3).reshape(9),
                                       pose.orientation)
        np.testing.assert_almost_equal(0, pose.time)

    def test_orientation_is_initialized_correctly_by_rotation_matrix(self):
        q = quaternion.from_rotation_vector(np.random.random_sample(3))
        r: np.ndarray = quaternion.as_rotation_matrix(q)
        o = r.reshape(9)
        pose = Pose(rotation_matrix=r)

        np.testing.assert_array_almost_equal(r, pose.rotation_matrix)
        np.testing.assert_array_almost_equal(o, pose.orientation)
        np.testing.assert_array_almost_equal(
            np.asarray(q, np.quaternion).view((np.float64, 4)),
            np.asarray(pose.quaternion, np.quaternion).view((np.float64, 4)))
        np.testing.assert_almost_equal(np.zeros(3), pose.position)
        np.testing.assert_almost_equal(0, pose.time)

    def test_orientation_is_initialized_correctly_by_orientation(self):
        q = quaternion.from_rotation_vector(np.random.random_sample(3))
        r: np.ndarray = quaternion.as_rotation_matrix(q)
        o = r.reshape(9)
        pose = Pose(orientation=o)

        np.testing.assert_array_almost_equal(r, pose.rotation_matrix)
        np.testing.assert_array_almost_equal(o, pose.orientation)
        np.testing.assert_array_almost_equal(
            np.asarray(q, np.quaternion).view((np.float64, 4)),
            np.asarray(pose.quaternion, np.quaternion).view((np.float64, 4)))
        np.testing.assert_almost_equal(np.zeros(3), pose.position)
        np.testing.assert_almost_equal(0, pose.time)

    def test_orientation_is_initialized_correctly_by_quaternin(self):
        q: np.ndarray = quaternion.from_rotation_vector(
            np.random.random_sample(3))
        r = quaternion.as_rotation_matrix(q)
        pose = Pose(quaternion=q)

        np.testing.assert_array_almost_equal(
            np.asarray(q, np.quaternion).view((np.float64, 4)),
            np.asarray(pose.quaternion, np.quaternion).view((np.float64, 4)))
        np.testing.assert_array_almost_equal(r, pose.rotation_matrix)
        np.testing.assert_array_almost_equal(r.reshape(9), pose.orientation)
        np.testing.assert_almost_equal(np.zeros(3), pose.position)
        np.testing.assert_almost_equal(0, pose.time)

    def test_pose_to_str(self):
        t = np.random.random_sample()
        p = np.random.rand(3)
        o: np.ndarray = quaternion.as_rotation_matrix(
            quaternion.from_rotation_vector(np.random.random_sample(3)))

        pose = Pose(position=p, rotation_matrix=o, time=t)

        expected = np.array2string(np.hstack([t, p, o.reshape(9)]),
                                   separator=',',
                                   formatter={'float_kind': lambda x: "%.2f" %
                                                                      x})[1:-1]
        np.testing.assert_array_almost_equal(p, pose.position)
        np.testing.assert_array_almost_equal(o, pose.rotation_matrix)
        np.testing.assert_array_almost_equal(o.reshape(9),
                                             pose.orientation)
        np.testing.assert_almost_equal(t, pose.time)
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
