import numpy as np
import pytest

import cdpyr


class PoseTestSuite(object):

    def test_pose_transformation_instances(self, empty_pose: cdpyr.motion.Pose):
        assert isinstance(empty_pose.linear,
                          cdpyr.kinematics.transformation.Linear)
        assert isinstance(empty_pose.angular,
                          cdpyr.kinematics.transformation.Angular)
        assert empty_pose.time is np.nan

    def test_getset_linear_position(self, rand_pose_3d: cdpyr.motion.Pose,
                                    rand_vector_3d):
        # access through the "linear" property and assert
        pos = rand_pose_3d.linear.position
        assert isinstance(pos, np.ndarray)
        assert pos.ndim == 1
        assert pos.shape == (3,)

        # access through the "position" property and assert
        pos, _ = rand_pose_3d.position
        assert isinstance(pos, np.ndarray)
        assert pos.ndim == 1
        assert pos.shape == (3,)

        # set property through the "linear" property
        rand_pose_3d.linear.position = rand_vector_3d
        # access through the "linear" property and assert
        pos = rand_pose_3d.linear.position
        assert isinstance(pos, np.ndarray)
        assert pos.ndim == 1
        assert pos.shape == (3,)
        assert pos == pytest.approx(rand_vector_3d)

        # access through the "position" property and assert
        pos, _ = rand_pose_3d.position
        assert isinstance(pos, np.ndarray)
        assert pos.ndim == 1
        assert pos.shape == (3,)
        assert pos == pytest.approx(rand_vector_3d)

    def test_getset_linear_velocity(self, rand_pose_3d: cdpyr.motion.Pose,
                                    rand_vector_3d):
        # access through the "linear" property and assert
        vel = rand_pose_3d.linear.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(np.asarray([0., 0., 0.]))

        # access through the "position" property and assert
        vel, _ = rand_pose_3d.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(np.asarray([0., 0., 0.]))

        # set property through the "linear" property
        rand_pose_3d.linear.velocity = rand_vector_3d
        # access through the "linear" property and assert
        vel = rand_pose_3d.linear.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(rand_vector_3d)

        # access through the "position" property and assert
        vel, _ = rand_pose_3d.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(rand_vector_3d)

    def test_getset_linear_acceleration(self,
                                        rand_pose_3d: cdpyr.motion.Pose,
                                        rand_vector_3d):
        # access through the "linear" property and assert
        acc = rand_pose_3d.linear.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(np.asarray([0., 0., 0.]))

        # access through the "position" property and assert
        acc, _ = rand_pose_3d.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(np.asarray([0., 0., 0.]))

        # set property through the "linear" property
        rand_pose_3d.linear.acceleration = rand_vector_3d
        # access through the "linear" property and assert
        acc = rand_pose_3d.linear.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(rand_vector_3d)

        # access through the "acceleration" property and assert
        acc, _ = rand_pose_3d.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(rand_vector_3d)

    def test_getset_angular_position(self, rand_pose_3d: cdpyr.motion.Pose,
                                     rand_rot):
        # access through the "angular" property and assert
        dcm = rand_pose_3d.angular.dcm
        assert isinstance(dcm, np.ndarray)
        assert dcm.ndim == 2
        assert dcm.shape == (3, 3)

        # access through the "position" property and assert
        _, dcm = rand_pose_3d.position
        assert isinstance(dcm, np.ndarray)
        assert dcm.ndim == 2
        assert dcm.shape == (3, 3)

        # set property through the "angular" property
        rand_pose_3d.angular.dcm = rand_rot
        # access through the "angular" property and assert
        dcm = rand_pose_3d.angular.dcm
        assert isinstance(dcm, np.ndarray)
        assert dcm.ndim == 2
        assert dcm.shape == (3, 3)
        assert dcm == pytest.approx(rand_rot)

        # access through the "position" property and assert
        _, dcm = rand_pose_3d.position
        assert isinstance(dcm, np.ndarray)
        assert dcm.ndim == 2
        assert dcm.shape == (3, 3)
        assert dcm == pytest.approx(rand_rot)

    def test_getset_angular_velocity(self, rand_pose_3d: cdpyr.motion.Pose,
                                     rand_vector_3d):
        # access through the "angular_velocity" property and assert
        vel = rand_pose_3d.angular.angular_velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(np.asarray([0., 0., 0.]))

        # access through the "position" property and assert
        _, vel = rand_pose_3d.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(np.asarray([0., 0., 0.]))

        # set property through the "velocity" property
        rand_pose_3d.angular.angular_velocity = rand_vector_3d
        # access through the "velocity" property and assert
        vel = rand_pose_3d.angular.angular_velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(rand_vector_3d)

        # access through the "position" property and assert
        _, vel = rand_pose_3d.velocity
        assert isinstance(vel, np.ndarray)
        assert vel.ndim == 1
        assert vel.shape == (3,)
        assert vel == pytest.approx(rand_vector_3d)

    def test_getset_angular_acceleration(self,
                                         rand_pose_3d: cdpyr.motion.Pose,
                                         rand_vector_3d):
        # access through the "velocity" property and assert
        acc = rand_pose_3d.angular.angular_acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(np.asarray([0., 0., 0.]))

        # access through the "position" property and assert
        _, acc = rand_pose_3d.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(np.asarray([0., 0., 0.]))

        # set property through the "velocity" property
        rand_pose_3d.angular.angular_acceleration = rand_vector_3d
        # access through the "velocity" property and assert
        acc = rand_pose_3d.angular.angular_acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(rand_vector_3d)

        # access through the "position" property and assert
        _, acc = rand_pose_3d.acceleration
        assert isinstance(acc, np.ndarray)
        assert acc.ndim == 1
        assert acc.shape == (3,)
        assert acc == pytest.approx(rand_vector_3d)

    def test_get_state(self, rand_pose_3d: cdpyr.motion.Pose):
        state_is = rand_pose_3d.state
        state_expected = np.hstack(
            (rand_pose_3d.linear.position, rand_pose_3d.angular.quaternion))

        assert state_is == pytest.approx(state_expected)

    def test_compare_two_poses_eq(self):
        pose_nan = cdpyr.motion.Pose()
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=0)

        assert pose_nan == pose_nan
        assert pose_0 == pose_1

    def test_compare_two_poses_ne(self):
        pose_none = cdpyr.motion.Pose()
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_none != pose_0
        assert pose_0 != pose_1

    def test_compare_two_poses_lt(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_0 < pose_1
        assert not pose_1 < pose_0

    def test_compare_two_poses_gt(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_1 > pose_0
        assert not pose_0 > pose_1

    def test_compare_two_poses_le(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_0 <= pose_1
        assert pose_1 <= pose_0

    def test_compare_two_poses_ge(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_1 >= pose_0
        assert pose_0 >= pose_1


if __name__ == "__main__":
    pytest.main()
