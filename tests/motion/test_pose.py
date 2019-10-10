import numpy as np
import pytest
from scipy.spatial.transform import Rotation

import cdpyr


class PoseTestSuite(object):

    def test_pose_transformation_instances(self, empty_pose: cdpyr.motion.Pose):
        assert isinstance(empty_pose.linear,
                          cdpyr.kinematics.transformation.Linear)
        assert isinstance(empty_pose.angular,
                          cdpyr.kinematics.transformation.Angular)
        assert empty_pose.time is None

    def test_getset_linear_position(self, rand_pose_3d: cdpyr.motion.Pose):
        pos = rand_pose_3d.linear.position

        assert pos.ndim == 1
        assert pos.shape == (3,)

        pos = np.random.random(3)
        rand_pose_3d.linear.position = pos

        assert rand_pose_3d.linear.position == pytest.approx(pos)
        assert rand_pose_3d.position[0] == pytest.approx(pos)

    def test_getset_linear_velocity(self, rand_pose_3d: cdpyr.motion.Pose):
        vel = rand_pose_3d.linear.velocity

        assert vel.ndim == 1
        assert vel.shape == (3,)

        vel = np.random.random(3)
        rand_pose_3d.linear.velocity = vel

        assert rand_pose_3d.linear.velocity == pytest.approx(vel)
        assert rand_pose_3d.velocity[0] == pytest.approx(vel)

    def test_getset_linear_acceleration(self,
                                        rand_pose_3d: cdpyr.motion.Pose):
        acc = rand_pose_3d.linear.acceleration

        assert acc.ndim == 1
        assert acc.shape == (3,)

        acc = np.random.random(3)
        rand_pose_3d.linear.acceleration = acc

        assert rand_pose_3d.linear.acceleration == pytest.approx(acc)
        assert rand_pose_3d.acceleration[0] == pytest.approx(acc)

    def test_getset_angular_position(self, rand_pose_3d: cdpyr.motion.Pose):
        dcm = rand_pose_3d.angular.dcm

        assert dcm.ndim == 2
        assert dcm.shape == (3, 3)

        dcm = Rotation.random().as_dcm()
        rand_pose_3d.angular.dcm = dcm

        assert rand_pose_3d.angular.dcm == pytest.approx(dcm)
        assert rand_pose_3d.position[1] == pytest.approx(dcm)

    def test_getset_angular_velocity(self, rand_pose_3d: cdpyr.motion.Pose):
        vel = rand_pose_3d.angular.angular_velocity

        assert vel.ndim == 1
        assert vel.shape == (3,)

        vel = np.random.random(3)
        rand_pose_3d.angular.angular_velocity = vel

        assert rand_pose_3d.angular.angular_velocity == pytest.approx(vel)
        assert rand_pose_3d.velocity[1] == pytest.approx(vel)

    def test_getset_angular_acceleration(self,
                                         rand_pose_3d: cdpyr.motion.Pose):
        acc = rand_pose_3d.angular.angular_acceleration

        assert acc.ndim == 1
        assert acc.shape == (3,)

        acc = np.random.random(3)
        rand_pose_3d.angular.angular_acceleration = acc

        assert rand_pose_3d.angular.angular_acceleration == pytest.approx(acc)
        assert rand_pose_3d.acceleration[1] == pytest.approx(acc)

    def test_get_state(self, rand_pose_3d: cdpyr.motion.Pose):
        state_is = rand_pose_3d.state
        state_expected = np.hstack(
            (rand_pose_3d.linear.position, rand_pose_3d.angular.quaternion))

        assert state_is == pytest.approx(state_expected)

    def test_compare_two_poses_eq(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=0)

        assert pose_0 == pose_1
        assert pose_0 == 0
        assert (pose_0 == 'int') == False

    def test_compare_two_poses_ne(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_0 != pose_1
        assert pose_0 != 1
        assert pose_0 != 'int'

    def test_compare_two_poses_lt(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_0 < pose_1
        assert pose_0 < 1
        with pytest.raises(TypeError):
            assert pose_0 < 'int'

    def test_compare_two_poses_gt(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_1 > pose_0
        assert pose_1 > 0
        with pytest.raises(TypeError):
            assert pose_1 > 'int'

    def test_compare_two_poses_le(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_0 <= pose_1
        assert pose_0 <= 1
        with pytest.raises(TypeError):
            assert pose_0 <= 'int'

    def test_compare_two_poses_ge(self):
        pose_0 = cdpyr.motion.Pose(time=0)
        pose_1 = cdpyr.motion.Pose(time=1)

        assert pose_1 >= pose_0
        assert pose_1 >= 0
        with pytest.raises(TypeError):
            assert pose_1 >= 'int'
