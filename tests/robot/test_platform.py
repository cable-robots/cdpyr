from __future__ import annotations

import numpy as np
import pytest

import cdpyr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformTestSuite(object):

    def test_wrench_1t_zero_pose(self,
                                  robot_1t: 'cdpyr.robot.Robot',
                                  zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [-9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:1, 0:1].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (1,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_1t_zero_pose_nonzero_cog(self,
                                              robot_1t: 'cdpyr.robot.Robot',
                                              zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [-9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:1, 0:1].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (1,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_1t_random_pose(self,
                                   robot_1t: 'cdpyr.robot.Robot',
                                   rand_pose_1t: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [-9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:1, 0:1].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (1,)
        assert platform.gravitational_wrench(rand_pose_1t, gravity) == pytest.approx(wrench)

    def test_wrench_1t_random_pose_nonzero_cog(self,
                                               robot_1t: 'cdpyr.robot.Robot',
                                               rand_pose_1t:
                                               'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [-9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:1, 0:1].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (1,)
        assert platform.gravitational_wrench(rand_pose_1t, gravity) == pytest.approx(wrench)

    def test_wrench_2t_zero_pose(self,
                                  robot_2t: 'cdpyr.robot.Robot',
                                  zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (2,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_2t_zero_pose_nonzero_cog(self,
                                              robot_2t: 'cdpyr.robot.Robot',
                                              zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (2,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_2t_random_pose(self,
                                   robot_2t: 'cdpyr.robot.Robot',
                                   rand_pose_2t: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (2,)
        assert platform.gravitational_wrench(rand_pose_2t, gravity) == pytest.approx(wrench)

    def test_wrench_2t_random_pose_nonzero_cog(self,
                                               robot_2t: 'cdpyr.robot.Robot',
                                               rand_pose_2t:
                                               'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (2,)
        assert platform.gravitational_wrench(rand_pose_2t, gravity) == pytest.approx(wrench)

    def test_wrench_3t_zero_pose(self,
                                  robot_3t: 'cdpyr.robot.Robot',
                                  zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia.dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_3t_zero_pose_nonzero_cog(self,
                                              robot_3t: 'cdpyr.robot.Robot',
                                              zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia.dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_3t_random_pose(self,
                                   robot_3t: 'cdpyr.robot.Robot',
                                   rand_pose_3t):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia.dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(rand_pose_3t, gravity) == pytest.approx(wrench)

    def test_wrench_3t_random_pose_nonzero_cog(self,
                                               robot_3t: 'cdpyr.robot.Robot',
                                               rand_pose_3t):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # manual wrench
        wrench = np.asarray((platform.linear_inertia.dot(gravity)))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(rand_pose_3t, gravity) == pytest.approx(wrench)

    def test_wrench_1r2t_zero_pose(self,
                                    robot_1r2t: 'cdpyr.robot.Robot',
                                    zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1r2t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity))),
            np.asarray([0.0])
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_1r2t_zero_pose_nonzero_cog(self,
                                                robot_1r2t: 'cdpyr.robot.Robot',
                                                zero_pose:
                                                'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1r2t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # get pose position
        _, rot = zero_pose.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity))),
            np.cross(
                rot[0:2, 0:2].dot(platform.center_of_gravity[0:2]),
                platform.linear_inertia[0:2, 0:2].dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_1r2t_random_pose(self,
                                     robot_1r2t: 'cdpyr.robot.Robot',
                                     rand_pose_1r2t: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1r2t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # get pose position
        _, rot = rand_pose_1r2t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity))),
            np.cross(
                rot[0:2, 0:2].dot(platform.center_of_gravity[0:2]),
                platform.linear_inertia[0:2, 0:2].dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(rand_pose_1r2t, gravity) == pytest.approx(wrench)

    def test_wrench_1r2t_random_pose_nonzero_cog(self,
                                                 robot_1r2t:
                                                 'cdpyr.robot.Robot',
                                                 rand_pose_1r2t:
                                                 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_1r2t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, -9.81]

        # get pose position
        _, rot = rand_pose_1r2t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia[0:2, 0:2].dot(gravity))),
            np.cross(
                rot[0:2, 0:2].dot(platform.center_of_gravity[0:2]),
                platform.linear_inertia[0:2, 0:2].dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (3,)
        assert platform.gravitational_wrench(rand_pose_1r2t, gravity) == pytest.approx(wrench)

    def test_wrench_2r3t_zero_pose(self,
                                    robot_2r3t: 'cdpyr.robot.Robot',
                                    zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2r3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.asarray([0.0, 0.0])
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (5,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_2r3t_zero_pose_nonzero_cog(self,
                                                robot_2r3t: 'cdpyr.robot.Robot',
                                                zero_pose:
                                                'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2r3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # get pose position
        _, rot = zero_pose.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )[0:2]
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (5,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_2r3t_random_pose(self,
                                     robot_2r3t: 'cdpyr.robot.Robot',
                                     rand_pose_2r3t: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2r3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # get pose position
        _, rot = rand_pose_2r3t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )[0:2]
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (5,)
        assert platform.gravitational_wrench(rand_pose_2r3t, gravity) == pytest.approx(wrench)

    def test_wrench_2r3t_random_pose_nonzero_cog(self,
                                                 robot_2r3t:
                                                 'cdpyr.robot.Robot',
                                                 rand_pose_2r3t:
                                                 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_2r3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0.0, 0.0, -9.81]

        # get pose position
        _, rot = rand_pose_2r3t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )[0:2]
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (5,)
        assert platform.gravitational_wrench(rand_pose_2r3t, gravity) == pytest.approx(wrench)

    def test_wrench_3r3t_zero_pose(self,
                                    robot_3r3t: 'cdpyr.robot.Robot',
                                    zero_pose: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3r3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0, 0, -9.81]

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.asarray([0.0, 0.0, 0.0])
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (6,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_3r3t_zero_pose_nonzero_cog(self,
                                                robot_3r3t: 'cdpyr.robot.Robot',
                                                zero_pose:
                                                'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3r3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0, 0, -9.81]

        # get pose position
        _, rot = zero_pose.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (6,)
        assert platform.gravitational_wrench(zero_pose, gravity) == pytest.approx(wrench)

    def test_wrench_3r3t_random_pose(self,
                                     robot_3r3t: 'cdpyr.robot.Robot',
                                     rand_pose_3r3t: 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3r3t.platforms[0]
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0, 0, -9.81]

        # get pose position
        _, rot = rand_pose_3r3t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (6,)
        assert platform.gravitational_wrench(rand_pose_3r3t, gravity) == pytest.approx(wrench)

    def test_wrench_3r3t_random_pose_nonzero_cog(self,
                                                 robot_3r3t:
                                                 'cdpyr.robot.Robot',
                                                 rand_pose_3r3t:
                                                 'cdpyr.motion.Pose'):
        # get the first platform
        platform: cdpyr.robot.Platform = robot_3r3t.platforms[0]
        platform.center_of_gravity = 0.3 * np.random.random((3,))
        # set mass of platform to 5 kg
        platform.linear_inertia = np.diag(np.full((3,), 5))
        # gravity scalar
        gravity = [0, 0, -9.81]

        # get pose position
        _, rot = rand_pose_3r3t.position

        # manual wrench
        wrench = np.hstack((
            np.asarray((platform.linear_inertia.dot(gravity))),
            np.cross(
                rot.dot(platform.center_of_gravity),
                platform.linear_inertia.dot(gravity)
            )
        ))

        assert wrench.ndim == 1
        assert wrench.shape == (6,)
        assert platform.gravitational_wrench(rand_pose_3r3t, gravity) == pytest.approx(wrench)


if __name__ == "__main__":
    pytest.main()
